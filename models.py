from pydantic import BaseModel, Field
from typing import Optional, Literal

class WorkoutBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the exercise")
    muscleGroup: str
    difficulty: Literal['Beginner', 'Intermediate', 'Advanced']
    duration: int = Field(..., gt=0, description="Duration in minutes")
    sets: int = Field(..., gt=0)
    reps: int = Field(..., gt=0)
    gifUrl: str
    description: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    pass

class WorkoutUpdate(BaseModel):
    name: Optional[str] = None
    muscleGroup: Optional[str] = None
    difficulty: Optional[Literal['Beginner', 'Intermediate', 'Advanced']] = None
    duration: Optional[int] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    gifUrl: Optional[str] = None
    liked: Optional[bool] = None
    description: Optional[str] = None

class WorkoutResponse(WorkoutBase):
    id: str
    liked: bool
