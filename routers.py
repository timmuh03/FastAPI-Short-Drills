from schemas import NoteCreate
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from db import get_db
from models import Note


router = APIRouter()


@router.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
  db_note = Note(text=note.text)
  
  db.add(db_note)
  db.commit()
  db.refresh(db_note)
  
  return {
    "message":"Note Created",
    "note_id": db_note.id,
    "note": db_note.text,
  }

@router.get("/notes")
def get_notes(db: Session = Depends(get_db)):
   
   notes = db.scalars(select(Note)).all()
   return notes