import re
from typing import Any

from pydantic import BaseModel, field_validator

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ClientBase(BaseModel):
    name: str
    address: str
    email: str
    notes: str

    @field_validator("name", "address", "email", "notes", mode="before")
    @classmethod
    def strip_and_require(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise ValueError("Must be a string")
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Must not be empty")
        return trimmed

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not EMAIL_PATTERN.match(value):
            raise ValueError("Invalid email format")
        return value


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    pass


class ClientOut(ClientBase):
    id: int
    created_at: str
    updated_at: str
