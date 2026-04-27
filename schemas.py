from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Data validation

# Schema/form for creating a new task
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

# Schema/form for API's structured output responses
class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    description: Optional[str]
    created_at: datetime

    # configuration of SQLAlchemy model to match schema
    class Config:
        from_attributes = True
