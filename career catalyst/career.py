from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import CareerHistory
from pydantic import BaseModel

router = APIRouter()

class CareerSave(BaseModel):
    user_email: str
    chat_history: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/save_career/")
def save_career(data: CareerSave, db: Session = Depends(get_db)):
    new_career = CareerHistory(user_id=data.user_email, chat_history=data.chat_history)
    db.add(new_career)
    db.commit()
    return {"message": "Career roadmap saved!"}
