from enum import Enum
from typing import Any

from pydantic import BaseModel, field_validator


class ContactMethod(str, Enum):
    email = "email"
    whatsapp = "whatsapp"
    discord = "discord"


MAX_CLIENT_NAME_LENGTH = 256
MAX_CLIENT_ADDRESS_LENGTH = 256
MAX_CLIENT_CITY_LENGTH = 128
MAX_CLIENT_COUNTRY_LENGTH = 128
MAX_CLIENT_MAIN_CONTACT_LENGTH = 256
MAX_CLIENT_ADDITIONAL_CONTACT_LENGTH = 256
MAX_CLIENT_ICO_LENGTH = 32
MAX_CLIENT_DIC_LENGTH = 32
MAX_CLIENT_NOTES_LENGTH = 1024


def _validate_length(value: str, max_len: int, label: str) -> str:
    if len(value) > max_len:
        raise ValueError(f"{label} must be at most {max_len} characters")
    return value


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

    @field_validator("name")
    @classmethod
    def validate_name_length(cls, value: str) -> str:
        return _validate_length(value, MAX_CLIENT_NAME_LENGTH, "Name")

    @field_validator("address")
    @classmethod
    def validate_address_length(cls, value: str) -> str:
        return _validate_length(value, MAX_CLIENT_ADDRESS_LENGTH, "Address")

    @field_validator("city")
    @classmethod
    def validate_city_length(cls, value: str) -> str:
        return _validate_length(value, MAX_CLIENT_CITY_LENGTH, "City")

    @field_validator("country")
    @classmethod
    def validate_country_length(cls, value: str) -> str:
        return _validate_length(value, MAX_CLIENT_COUNTRY_LENGTH, "Country")

    @field_validator("main_contact")
    @classmethod
    def validate_main_contact_length(cls, value: str) -> str:
        return _validate_length(value, MAX_CLIENT_MAIN_CONTACT_LENGTH, "Main contact")


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

    @field_validator("additional_contact")
    @classmethod
    def validate_additional_contact_length(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _validate_length(
            value, MAX_CLIENT_ADDITIONAL_CONTACT_LENGTH, "Additional contact"
        )

    @field_validator("ico")
    @classmethod
    def validate_ico_length(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _validate_length(value, MAX_CLIENT_ICO_LENGTH, "ICO")

    @field_validator("dic")
    @classmethod
    def validate_dic_length(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _validate_length(value, MAX_CLIENT_DIC_LENGTH, "DIC")

    @field_validator("notes")
    @classmethod
    def validate_notes_length(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _validate_length(value, MAX_CLIENT_NOTES_LENGTH, "Notes")


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

    @field_validator("additional_contact")
    @classmethod
    def validate_additional_contact_length(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _validate_length(
            value, MAX_CLIENT_ADDITIONAL_CONTACT_LENGTH, "Additional contact"
        )

    @field_validator("ico")
    @classmethod
    def validate_ico_length(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _validate_length(value, MAX_CLIENT_ICO_LENGTH, "ICO")

    @field_validator("dic")
    @classmethod
    def validate_dic_length(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _validate_length(value, MAX_CLIENT_DIC_LENGTH, "DIC")

    @field_validator("notes")
    @classmethod
    def validate_notes_length(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _validate_length(value, MAX_CLIENT_NOTES_LENGTH, "Notes")


class ClientOut(ClientRequired):
    additional_contact: str | None = None
    ico: str | None = None
    dic: str | None = None
    notes: str | None = None
    favourite: bool
    id: str
    created_at: str
    updated_at: str
