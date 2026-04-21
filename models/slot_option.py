from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import (Mapped,
  mapped_column, relationship)

from models.base import Base



class SlotOption(Base):
  __tablename__ = "slot_options"

  id: Mapped[int] = (
    mapped_column(primary_key=True)
  )
  slot_id: Mapped[int] = (
    mapped_column(ForeignKey(
      "example_slots.id"))
  )
  option_text: Mapped[str] = (
    mapped_column(Text)
  )
  display_order: Mapped[int] = (
    mapped_column(default=0)
  )

  slot: Mapped["ExampleSlot"] = (
    relationship(
      back_populates="slot_options")
  )