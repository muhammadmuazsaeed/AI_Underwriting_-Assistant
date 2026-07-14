"""
SQLAlchemy models for storing properties, analyses, and chat history.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class PropertyAnalysis(Base):
    __tablename__ = "property_analyses"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Inputs
    purchase_price = Column(Float)
    down_payment = Column(Float)
    monthly_rent = Column(Float)
    vacancy_rate = Column(Float)
    property_tax = Column(Float)
    insurance = Column(Float)
    maintenance = Column(Float)
    utilities = Column(Float)
    management_fee = Column(Float)
    other_expenses = Column(Float)

    # Results
    noi = Column(Float)
    cash_flow = Column(Float)
    cap_rate = Column(Float)
    roi = Column(Float)
    risk_level = Column(String(20))
    risk_flags = Column(Text)  # stored as comma-separated string

    chat_messages = relationship("ChatMessage", back_populates="analysis")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer, ForeignKey("property_analyses.id"))
    role = Column(String(20))   # "user" or "assistant"
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    analysis = relationship("PropertyAnalysis", back_populates="chat_messages")
