import logging

from fastapi import (APIRouter, Depends,
  HTTPException, status)
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_db
from models.slot_option import (
  SlotOption)
from models.example_slot import(
  ExampleSlot)
from schemas.slot_option import (
  SlotOptionCreate,
  SlotOptionReadUp, 
  SlotOptionRead,
  SlotOptionUpdate)

logger = logging.getLogger(__name__)

router = APIRouter(
  tags=["Slot Options"])

@router.post("/slots/{slot_id}/options",
  response_model=SlotOptionReadUp,
  status_code=status.HTTP_201_CREATED)
def create_slot_option(
  slot_id: int,
  option_data: SlotOptionCreate,
  db: Session = Depends(get_db),
):
  slot = db.scalar(select(
    ExampleSlot).where(
      ExampleSlot.id == slot_id)
  )

  if not slot:
    raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Slot not found",
    )

  option = SlotOption(
    option_text=option_data.option_text,
    slot_id=slot_id
  )

  db.add(option)
  db.commit()
  db.refresh(option)

  return option

@router.delete("/options/{option_id}",
  status_code=status.HTTP_204_NO_CONTENT)
def delete_slot_option(
  option_id: int,
  db: Session = Depends(get_db),
):
  option = db.scalar(select(
    SlotOption).where(
    SlotOption.id == option_id)
  )

  if not option:
    raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
      detail="Option not found",)

  db.delete(option)
  db.commit()

@router.patch("/options/{option_id}",
  response_model=SlotOptionReadUp,
  status_code=status.HTTP_200_OK)
def update_slot_option(
  option_id: int,
  option_update: SlotOptionUpdate,
  db: Session = Depends(get_db),
):
  option = db.scalar(select(
    SlotOption).where(
      SlotOption.id == option_id)
  )

  if not option:
    raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Option not found")

  if option_update.option_text is not None:
    option.option_text = (
      option_update.option_text)
  if (
    option_update.slot_id 
    is not None):
    slot = db.scalar(select(
      ExampleSlot).where(
      ExampleSlot.id == (
      option_update.slot_id))
    )
    if not slot:
      raise HTTPException(
      status_code=(
        status.HTTP_404_NOT_FOUND),
      detail="Slot not found",
      )
      
    
    option.slot_id = option_update.slot_id

  db.commit()
  db.refresh(option)

  return option

@router.get("/slots/{slot_id}/options",
  response_model=list[SlotOptionRead],
  status_code=status.HTTP_200_OK)
def get_slot_options(
  slot_id: int,
  db: Session = Depends(get_db),
):
  slot = db.scalar(select(
    ExampleSlot).where(
    ExampleSlot.id == slot_id)
  )

  if not slot:
    raise HTTPException(
      status_code=(
        status.HTTP_404_NOT_FOUND),
      detail="Slot not found",
    )

  options = db.scalars(select(
    SlotOption).where(
    SlotOption.slot_id == slot_id)
  ).all()

  if not options:
    logger.info("No options found")

  return options