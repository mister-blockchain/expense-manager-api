from pydantic import BaseModel, field_validator, Field, model_validator
import re


# ==========================================
# Shared Validator Functions
# ==========================================

def validate_description(value: str) -> str:
    """Shared validation for description field"""
    value = value.strip()
    value = re.sub(r"\s+", " ", value)
    
    if not re.search(r"[A-Za-z]", value):
        raise ValueError("Description must contain at least one letter")
    
    return value


def validate_amount(value: float) -> float:
    """Shared validation for amount field"""
    value = round(value, 2)
    
    if value <= 0:
        raise ValueError("Amount must be greater than zero")
    
    return value


# ==========================================
# Shared Field Definitions
# ==========================================

DESCRIPTION_FIELD = Field(
    ...,
    min_length=2,
    max_length=100,
    examples=["Groceries"],
    description="What was the expense for?"
)

AMOUNT_FIELD = Field(
    ...,
    gt=0,
    le=1_000_000,
    examples=[25.99],
    description="How much did it cost?"
)

ID_FIELD = Field(
    ...,
    ge=1,
    examples=[1],
    description="Unique expense ID"
)


# ==========================================
# Base Class with Validators (Fixed)
# ==========================================

class ExpenseBase(BaseModel):
    """Base schema with shared fields and validators"""
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


# ==========================================
# Schemas
# ==========================================

class ExpenseCreate(ExpenseBase):
    """Schema for creating an expense (POST)"""
    pass


class ExpenseUpdate(ExpenseBase):
    """Schema for updating an expense (PUT)"""
    pass


class ExpenseResponse(BaseModel):
    """Schema for expense response (GET)"""
    id: int = ID_FIELD
    description: str = DESCRIPTION_FIELD
    amount: float = AMOUNT_FIELD


class SummaryResponse(BaseModel):
    """Schema for summary response"""
    total_expenses: int = Field(..., examples=[5])
    total_amount: float = Field(..., examples=[125.75])
    average_amount: float = Field(..., examples=[25.15])


class DeleteResponse(BaseModel):
    """Schema for delete response"""
    message: str = Field(..., examples=["Expense 1 deleted successfully"])
    deleted_expense: ExpenseResponse


class UpdateResponse(BaseModel):
    """Schema for update response"""
    message: str = Field(..., examples=["Expense 1 updated successfully"])
    expense: ExpenseResponse