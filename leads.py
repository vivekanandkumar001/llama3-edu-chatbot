import re
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DB_PATH

Base = declarative_base()
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    course = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[- ]?)?(?:\d{10}|\d{3}[- ]\d{3}[- ]\d{4})")

def extract_contact(text: str):
    emails = EMAIL_RE.findall(text or "")
    phones = PHONE_RE.findall(text or "")
    return (emails[0] if emails else None, phones[0] if phones else None)

def save_lead(name=None, email=None, phone=None, course=None):
    with SessionLocal() as db:
        lead = Lead(name=name, email=email, phone=phone, course=course)
        db.add(lead)
        db.commit()
        return True
