from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from enum import Enum

class CaseStatusEnum(str, Enum):
    NEW = "New"
    IN_FOLLOW_UP = "In Follow-up"
    PARTIALLY_PAID = "Partially Paid"
    CLOSED = "Closed"

class CaseBase(BaseModel):
    invoice_number: str
    invoice_amount: float = Field(..., gt=0)
    invoice_date: date
    due_date: date

class CaseCreate(CaseBase):
    client_id: int

class CaseUpdate(BaseModel):
    status: Optional[CaseStatusEnum] = None
    last_follow_up_notes: Optional[str] = None

class CaseResponse(CaseBase):
    id: int
    client_id: int
    status: CaseStatusEnum
    last_follow_up_notes: Optional[str]
    
    class Config:
        from_attributes = True

class ClientBase(BaseModel):
    client_name: str = Field(..., min_length=2, max_length=100)
    company_name: str = Field(..., min_length=2, max_length=150)
    city: str = Field(..., min_length=2, max_length=100)
    contact_person: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str

    @field_validator('phone')
    @classmethod
    def validate_indian_phone(cls, v: str) -> str:
        # It substitutes any non-digit character with an empty string.
        # \D is a special character in regex that matches any non-digit character.
        # v is the raw phone input from the user.
        clean_phone = re.sub(r'\D', '', v) 
        # It validates the length of the cleaned phone number.
        if len(clean_phone) < 10 or len(clean_phone) > 13: 
            raise ValueError('Invalid phone number format')
        return clean_phone

class ClientCreate(ClientBase):
    pass 

class ClientResponse(ClientBase):
    id: int
    
    class Config:
        from_attributes = True # Enables SQLAlchemy model conversion