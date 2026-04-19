from pydantic import BaseModel

class ConceptCreate(BaseModel):
  term: str
  description: str

class ExampleTemplateCreate(BaseModel):
  title: str
  template_text: str | None = None
  display_order: int = 0

class ExampleSlotCreate(BaseModel):
  slot_label: str
  slot_type: str

class SlotOptionCreate(BaseModel):
  option_text: str
  display_order: int = 0

# vvv read down vvv

class ConceptReadDown(ConceptCreate):
  id: int
  examples: list["ExampleTemplateReadDown"]

  model_config = {"from_attributes": True}

class ExampleTemplateReadDown(
  ExampleTemplateCreate):
  id: int
  concept_id: int
  slots: list["ExampleSlotReadDown"]

  model_config = {"from_attributes": True}

class ExampleSlotReadDown(
  ExampleSlotCreate):
  id: int
  template_id: int
  slot_options: list["SlotOptionRead"]

  model_config = {"from_attributes": True}

class SlotOptionRead(SlotOptionCreate):
  id: int
  slot_id: int

  model_config = {"from_attributes": True}

# vvv read up vvv

class ConceptRead(ConceptCreate):
  id: int

  model_config = {"from_attributes": True}

class ExampleTemplateReadUp(
  ExampleTemplateCreate):
  id: int
  concept_id: int
  concept: ConceptRead

  model_config = {"from_attributes": True}

class ExampleSlotReadUp(ExampleSlotCreate):
  id: int
  template_id: int
  template: ExampleTemplateReadUp

  model_config = {"from_attributes": True}

class SlotOptionReadUp(SlotOptionCreate):
  id:  int
  slot_id: int
  slot: ExampleSlotReadUp

  model_config = {"from_attributes": True}

