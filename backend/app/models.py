from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=True)
    source = Column(String, default="web")  # web, whatsapp
    contact_info = Column(String, nullable=True)
    status = Column(String, default="open") # open, in_progress, resolved, closed
    created_at = Column(DateTime, default=datetime.utcnow)

    # Evidence (One-to-Many)
    evidence = relationship("Evidence", back_populates="complaint")

    # Ticket (One-to-One)
    ticket = relationship("Ticket", back_populates="complaint", uselist=False)

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"))
    file_path = Column(String)
    media_type = Column(String) # image, video, audio
    created_at = Column(DateTime, default=datetime.utcnow)

    complaint = relationship("Complaint", back_populates="evidence")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), unique=True)
    issue_type = Column(String, nullable=True) # garbage, pothole, illegal_dumping
    priority = Column(String, default="medium")
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)

    complaint = relationship("Complaint", back_populates="ticket")
