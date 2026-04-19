from sqlalchemy import (ForeignKey, String, 
  Text)
from sqlalchemy.orm import (
  DeclarativeBase, 
  Mapped, mapped_column, relationship)

class Base(DeclarativeBase):
  pass

class Concept(Base):
  __tablename__ = "concepts"
  
  id: Mapped[int] = (
    mapped_column(primary_key=True))
  term: Mapped[str] = (
    mapped_column(unique=True))
  description: Mapped[str] = (
    mapped_column())
  examples: Mapped[list[
  "ExampleTemplate"]] = (
    relationship(back_populates="concept",
      cascade="all, delete-orphan")
  )

class ExampleTemplate(Base):
  __tablename__ = "example_templates"

  id: Mapped[int] = (
    mapped_column(primary_key=True)
  )
  concept_id: Mapped[int] = (mapped_column(
    ForeignKey("concepts.id"))
  )
  title: Mapped[str] = (
    mapped_column(String(100))
  )
  template_text: Mapped[str | None] = (
    mapped_column(Text, nullable=True)
  )
  display_order: Mapped[int] = (
    mapped_column(default=0)
  )

  concept: Mapped["Concept"] = (
    relationship(
      back_populates="examples")
  )
  slots: Mapped[list[
    "ExampleSlot"]] = (relationship(
       back_populates="template",
       cascade="all, delete-orphan")
  )

class ExampleSlot(Base):
  __tablename__ = "example_slots"
  
  id: Mapped[int] = (
    mapped_column(primary_key=True)
  )
  template_id: Mapped[int] = (
    mapped_column(ForeignKey(
                  "example_templates.id"))
  )
  slot_label: Mapped[str] = (
    mapped_column(String(50))
  )
  slot_type: Mapped[str] = (
    mapped_column(String(50))
  )
  
  template: Mapped["ExampleTemplate"] = (
    relationship(back_populates="slots")
  )
  slot_options: Mapped[list[
    "SlotOption"]] = (relationship(
    back_populates="slot", 
    cascade="all, delete-orphan")
  )

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