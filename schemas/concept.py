from pydantic import BaseModel



class ConceptCreate(BaseModel):
  term: str
  description: str

class ConceptReadDown(ConceptCreate):
  id: int
  examples: list["ExampleTemplateReadDown"]

  model_config = {"from_attributes": True}

class ConceptRead(ConceptCreate):
  id: int

  model_config = {"from_attributes": True}

class ConceptUpdate(BaseModel):
  term: str | None = None
  description: str | None = None