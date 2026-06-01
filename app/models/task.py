from sqlalchemy import Column,String,DateTime,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Task(Base):
    
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
 
    owner_id = Column(String, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")

