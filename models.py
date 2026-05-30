from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() # this is the base class for all models

class Client(Base): # this is a model for the clients table
    __tablename__ = "clients" # this is the name of the table in the database

    id = Column(Integer, primary_key=True, index=True) # this is the primary key for the table # Indexing is a technique used to speed up data retrieval operations on a database table
    client_name = Column(String(100), nullable=False)
    company_name = Column(String(150), unique=True, index=True, nullable=False)
    city = Column(String(100), nullable=False, index=True) # Indexed for operational filtering by city
    contact_person = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)

