from sqlalchemy import Column,String
from sqlalchemy.ext.declarative import declarative_base

# Base class for models
Base = declarative_base()

class Task(Base):
    
    __tablename__ = "TO DO list"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)