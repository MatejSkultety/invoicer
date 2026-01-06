from enum import Enum
from typing import Any

from pydantic import BaseModel, field_validator


class ContactMethod(str, Enum):
    email = "email"
    whatsapp = "whatsapp"
    discord = "discord"


class ClientRequired(BaseModel):
    name: str
    address: str
    city: str
    country: str
    main_contact_method: ContactMethod
    main_contact: str

    @field_validator("name", "address", "city", "country", "main_contact", mode="before")
    @classmethod
    def strip_and_require(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise ValueError("Must be a string")
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Must not be empty")
        return trimmed

    @field_validator("main_contact_method", mode="before")
    @classmethod
    def normalize_contact_method(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip().lower()
        return value


class ClientCreate(ClientRequired):
    additional_contact: str | None = None
    ico: str | None = None
    dic: str | None = None
    notes: str | None = None
    favourite: bool = False

    @field_validator("additional_contact", "ico", "dic", "notes", mode="before")
    @classmethod
    def strip_optional(cls, value: Any) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("Must be a string")
        trimmed = value.strip()
        return trimmed or None


class ClientUpdate(ClientRequired):
    additional_contact: str | None
    ico: str | None
    dic: str | None
    notes: str | None
    favourite: bool

    @field_validator("additional_contact", "ico", "dic", "notes", mode="before")
    @classmethod
    def strip_optional(cls, value: Any) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("Must be a string")
        trimmed = value.strip()
        return trimmed or None


class ClientOut(ClientRequired):
    additional_contact: str | None = None
    ico: str | None = None
    dic: str | None = None
    notes: str | None = None
    favourite: bool
    id: int
    created_at: str
    updated_at: str
