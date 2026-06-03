from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List 
import backend.models
import backend.schemas
from backend.database import SessionLocal, get_db

# Create a prefix for the endpoints instead of writing it in every endpoint. 
# tags is used to group the endpoints in the swagger ui.
router = APIRouter(prefix="/api/clients", tags=["Client Management"])

@router.post("/", response_model=backend.schemas.ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client: backend.schemas.ClientCreate, db: Session = Depends(get_db)):
    # Check for existing unique fields to prevent unhandled database integrity crashes
    db_client = db.query(backend.models.Client).filter(
        (backend.models.Client.email == client.email) | 
        (backend.models.Client.company_name == client.company_name) |
        (backend.models.Client.phone == client.phone)
    ).first()
    
    if db_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A client with this company name, email, or phone already exists."
        )
    #Converts the pydantic ClientCreate object into a plain Python dictionary.
    new_client = backend.models.Client(**client.model_dump())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@router.get("/", response_model=List[backend.schemas.ClientResponse])
def list_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    #It uses the offset and limit parameters to skip a certain number of records and limit the number of records returned.
    clients = db.query(backend.models.Client).offset(skip).limit(limit).all() 
    return clients

