from pydantic import BaseModel, Field, validator
from typing import List, Optional

class TicketCreate(BaseModel):
    numbers: List[int] = Field(..., min_items=5, max_items=5)
    draw_id: int = Field(...)

    @validator('numbers')
    def validate_numbers(cls, v):
        if len(set(v)) != 5:
            raise ValueError("Числа должны быть уникальными.")
        if not all(1 <= num <= 36 for num in v):
            raise ValueError("Числа должны быть в диапазоне от 1 до 36.")
        return sorted(v)

class TicketResponse(BaseModel):
    id: int
    draw_id: int
    numbers: List[int]
    is_winner: bool

    @validator('numbers', pre=True)
    def parse_numbers_string(cls, v):
        if isinstance(v, str):
            return [int(x) for x in v.split(',')]
        return v

    class Config:
        from_attributes = True

class DrawCreateResponse(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True

class DrawResultResponse(BaseModel):
    id: int
    status: str
    winning_numbers: Optional[List[int]] = None
    tickets: List[TicketResponse] = []

    @validator('winning_numbers', pre=True)
    def parse_winning_numbers_string(cls, v):
        if isinstance(v, str) and v:
            return [int(x) for x in v.split(',')]
        return None

    class Config:
        from_attributes = True