from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Date, Text
from sqlalchemy.orm import relationship

Base = declarative_base()

class CaseStatus(str, enum.Enum):
    NEW = "New"
    IN_FOLLOW_UP = "In Follow-up"
    PARTIALLY_PAID = "Partially Paid"
    CLOSED = "Closed"

class RecoveryCase(Base):
    __tablename__ = "recovery_cases"

    id = Column(Integer, primary_key=True, index=True)
    # On delete Cascade ensures that if a client is deleted, all their recovery cases are also deleted. (Parent-Child relationship)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    
    invoice_number = Column(String(50), unique=True, index=True, nullable=False)
    invoice_amount = Column(Float, nullable=False)
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    
    status = Column(Enum(CaseStatus), default=CaseStatus.NEW, nullable=False)
    last_follow_up_notes = Column(Text, nullable=True)

    # Relationship back to the Client
    client = relationship("Client", back_populates="cases")

class Client(Base): 
    __tablename__ = "clients" 

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(100), nullable=False)
    company_name = Column(String(150), unique=True, index=True, nullable=False)
    city = Column(String(100), nullable=False, index=True) # Indexed for operational filtering by city
    contact_person = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)

    #This line defines a one-to-many relationship between "Client" and "RecoveryCase". 
    #It means one client can have many recovery cases. 
    cases = relationship("RecoveryCase", back_populates="client")

