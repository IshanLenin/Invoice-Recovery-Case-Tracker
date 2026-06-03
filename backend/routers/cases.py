from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import List, Optional
import backend.models
import backend.schemas
from backend.database import get_db


router = APIRouter(prefix="/api/cases", tags=["Case Management"])

@router.post("/", response_model=backend.schemas.CaseResponse, status_code=status.HTTP_201_CREATED)
def create_case(case: backend.schemas.CaseCreate, db: Session = Depends(get_db)):
    # Enforce linking to a valid client
    client = db.query(backend.models.Client).filter(backend.models.Client.id == case.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
        
    new_case = backend.models.RecoveryCase(**case.model_dump())
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    return new_case

@router.get("/", response_model=List[backend.schemas.CaseResponse])
def list_cases(
    db: Session = Depends(get_db),
    status: Optional[backend.schemas.CaseStatusEnum] = Query(None, description="Filter by case status"),
    sort_due_date: str = Query("asc", regex="^(asc|desc)$", description="Sort by due date")
):
    query = db.query(backend.models.RecoveryCase)
    
    # Apply Status Filter
    if status:
        query = query.filter(backend.models.RecoveryCase.status == status)
        
    # Apply Sorting
    if sort_due_date == "desc":
        query = query.order_by(desc(backend.models.RecoveryCase.due_date))
    else:
        query = query.order_by(asc(backend.models.RecoveryCase.due_date))
        
    return query.all()

@router.get("/{case_id}", response_model=backend.schemas.CaseResponse)
def get_case(case_id: int, db: Session = Depends(get_db)):
    """Fetch a single recovery case by its ID."""
    db_case = db.query(backend.models.RecoveryCase).filter(backend.models.RecoveryCase.id == case_id).first()
    
    if not db_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Case with ID {case_id} not found"
        )
        
    return db_case

@router.patch("/{case_id}", response_model=backend.schemas.CaseResponse)
def update_case(case_id: int, case_update: backend.schemas.CaseUpdate, db: Session = Depends(get_db)):
    db_case = db.query(backend.models.RecoveryCase).filter(backend.models.RecoveryCase.id == case_id).first()
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")

    #exclude_unset = True means only update the fields which the user explicitly mentioned.
    update_data = case_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_case, key, value)
    
    #Commit and refresh the changes made to the database.
    db.commit()
    db.refresh(db_case)
    return db_case