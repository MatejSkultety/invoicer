from typing import Any

from pydantic import BaseModel, field_validator

MAX_NAME_LENGTH = 256


class CatalogItemRequired(BaseModel):
    name: str
    description: str
    unit: str
    unit_price: int

    @field_validator("name", "description", "unit", mode="before")
    @classmethod
    def strip_and_require(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise ValueError("Must be a string")
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Must not be empty")
        return trimmed

    @field_validator("name")
    @classmethod
    def validate_name_length(cls, value: str) -> str:
        if len(value) > MAX_NAME_LENGTH:
            raise ValueError(f"Must be at most {MAX_NAME_LENGTH} characters")
        return value

    @field_validator("unit_price", mode="before")
    @classmethod
    def validate_unit_price(cls, value: Any) -> int:
        if isinstance(value, bool):
            raise ValueError("Must be an integer")
        if isinstance(value, float):
            if not value.is_integer():
                raise ValueError("Must be an integer")
            value = int(value)
        if not isinstance(value, int):
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValueError("Must be an integer") from None
        if value < 0:
            raise ValueError("Must be greater than or equal to 0")
        return value


class CatalogItemCreate(CatalogItemRequired):
    tax_rate: int | None = None

    @field_validator("tax_rate", mode="before")
    @classmethod
    def validate_tax_rate(cls, value: Any) -> int | None:
        if value is None:
            return None
        if isinstance(value, bool):
            raise ValueError("Must be an integer")
        if isinstance(value, float):
            if not value.is_integer():
                raise ValueError("Must be an integer")
            value = int(value)
        if not isinstance(value, int):
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValueError("Must be an integer") from None
        if value < 0:
            raise ValueError("Must be greater than or equal to 0")
        return value


class CatalogItemUpdate(CatalogItemRequired):
    tax_rate: int | None

    @field_validator("tax_rate", mode="before")
    @classmethod
    def validate_tax_rate(cls, value: Any) -> int | None:
        if value is None:
            return None
        if isinstance(value, bool):
            raise ValueError("Must be an integer")
        if isinstance(value, float):
            if not value.is_integer():
                raise ValueError("Must be an integer")
            value = int(value)
        if not isinstance(value, int):
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValueError("Must be an integer") from None
        if value < 0:
            raise ValueError("Must be greater than or equal to 0")
        return value


class CatalogItemOut(CatalogItemRequired):
    tax_rate: int | None = None
    id: str
    created_at: str
    updated_at: str
