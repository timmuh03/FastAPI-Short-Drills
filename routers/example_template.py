import logging

from fastapi import (APIRouter, Depends,
  HTTPException, status)
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_db
from models.concept import Concept
from models.example_template import (
  ExampleTemplate)
from schemas import (
  ExampleTemplateCreate,
  ExampleTemplateReadUp, 
  ExampleTemplateReadDown,
  ExampleTemplateUpdate)

logger = logging.getLogger(__name__)

router = APIRouter(
  tags=["Example Templates"])


@router.post("/concepts/{concept_id}/"
  "examples",
  response_model=ExampleTemplateReadUp,
  status_code=status.HTTP_201_CREATED)
def create_example_template(
  concept_id: int,
  example_template: ExampleTemplateCreate,
  db: Session = Depends(get_db),
):
  concept = db.scalar(
    select(Concept).where(
      Concept.id == concept_id))

  if not concept:
    raise HTTPException(
      status_code=status.
      HTTP_404_NOT_FOUND,
      detail="Concept not found",
    )

  template = ExampleTemplate(
    title=example_template.title,
    template_text=(
      example_template.template_text),
    display_order=(
      example_template.display_order),
    concept_id=concept_id,
  )

  db.add(template)
  db.commit()
  db.refresh(template)

  return template

@router.delete("/examples/{example_id}",
  status_code=status.HTTP_204_NO_CONTENT)
def delete_example_template(
  example_id: int,
  db: Session = Depends(get_db),
):
  example = db.scalar(select(
    ExampleTemplate).where(
      ExampleTemplate.id == example_id))

  if not example:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Example not found"
    )
    
  db.delete(example)
  db.commit()

@router.patch("/examples/{example_id}",
  response_model=ExampleTemplateReadUp,
  status_code=status.HTTP_200_OK)
def update_example_template(
  example_id: int,
  example_update: ExampleTemplateUpdate,
  db: Session = Depends(get_db),
):
  example = db.scalar(select(
    ExampleTemplate).where(
      ExampleTemplate.id == example_id)
  )

  if not example:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Example not found",
    )

  if example_update.title is not None:
    example.title = example_update.title
  if (
    example_update.template_text 
    is not None):
    example.template_text = (
      example_update.template_text)
  if (example_update.display_order
    is not None):
    example.display_order = (
      example_update.display_order)

  db.commit()
  db.refresh(example)
  
  return example

@router.get(
  "/concepts/{concept_id}/examples",
  response_model=list[
  ExampleTemplateReadDown],
  status_code=status.HTTP_200_OK)
def get_example_templates(
  concept_id: int,
  db: Session = Depends(get_db),
):
  concept = db.scalar(select(
    Concept).where(
    Concept.id == concept_id)
  )

  if not concept:
    raise HTTPException(
      status_code=(
      status.HTTP_404_NOT_FOUND),
      detail="Concept not found",
    )

  examples = db.scalars(select(
    ExampleTemplate).where(
    ExampleTemplate.concept_id ==
    concept_id)
  ).all()

  if not examples:
    logger.info("No examples found")
    
  return examples

  