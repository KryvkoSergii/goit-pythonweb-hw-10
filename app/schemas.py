from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List


class ContactBase(BaseModel):
    first_name: str = Field(description="Contact first name", max_length=100)
    last_name: str = Field(description="Contact last name", max_length=100)
    email: str = Field(
        max_length=50,
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        description="Contact email",
    )
    phone: str = Field(max_length=30, description="Contact phone")
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$", description="Contact birthday")
    notes: Optional[str] = Field(
        default=None, max_length=255, description="Contact notes"
    )


class ContractModel(ContactBase):
    id: int = Field(description="Identifier")


class ContactsQuery(BaseModel):
    skip: int
    limit: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None


class ErrorContent(BaseModel):
    message: str


class ErrorsContent(BaseModel):
    errors: List[ErrorContent]
