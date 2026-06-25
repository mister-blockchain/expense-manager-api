from datetime import datetime
from pydantic import BaseModel, field_validator, Field
import re


# ==========================================
# Shared Validator Functions
# ==========================================
def validate_description(value: str) -> str:
    value = value.strip()
    value = re.sub(r"\s+", " ", value)
    if not re.search(r"[A-Za-z]", value):
        raise ValueError("Description must contain at least one letter")
    return value


def validate_amount(value: float) -> float:
    value = round(value, 2)
    if value <= 0:
        raise ValueError("Amount must be greater than zero")
    return value


# ==========================================
# Shared Field Definitions
# ==========================================
DESCRIPTION_FIELD = Field(
    ..., min_length=2, max_length=100,
    examples=["Groceries"], description="What was the expense for?"
)

AMOUNT_FIELD = Field(
    ..., gt=0, le=1_000_000,
    examples=[25.99], description="How much did it cost?"
)


# ==========================================
# Base Schema
# ==========================================
class ExpenseBase(BaseModel):
    description: str = DESCRIPTION_FIELD
    amount: float = AMOUNT_FIELD

    @field_validator("description")
    @classmethod
    def check_description(cls, value: str) -> str:
        return validate_description(value)

    @field_validator("amount")
    @classmethod
    def check_amount(cls, value: float) -> float:
        return validate_amount(value)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    pass


class ExpenseResponse(BaseModel):
    id: int = Field(..., ge=1, examples=[1])
    description: str = DESCRIPTION_FIELD
    amount: float = AMOUNT_FIELD
    created_at: datetime | None = None

    class Config:
        from_attributes = True  # For SQLAlchemy compatibility


class SummaryResponse(BaseModel):
    total_expenses: int = Field(..., examples=[5])
    total_amount: float = Field(..., examples=[125.75])
    average_amount: float = Field(..., examples=[25.15])


class DeleteResponse(BaseModel):
    message: str
    deleted_expense: ExpenseResponse


class UpdateResponse(BaseModel):
    message: str
    expense: ExpenseResponse