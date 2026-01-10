from typing import Any

from pydantic import BaseModel, field_validator

MAX_NAME_LENGTH = 256
MAX_ADDRESS_LENGTH = 256
MAX_CITY_LENGTH = 128
MAX_COUNTRY_LENGTH = 128
MAX_TRADE_LICENSING_OFFICE_LENGTH = 256
MAX_EMAIL_LENGTH = 256
MAX_PHONE_LENGTH = 64
MAX_BANK_LENGTH = 256
MAX_IBAN_LENGTH = 34
MAX_SWIFT_LENGTH = 11
MAX_ICO_LENGTH = 32
MAX_DIC_LENGTH = 32


def _validate_length(value: str, max_len: int, label: str) -> str:
    if len(value) > max_len:
        raise ValueError(f"{label} must be at most {max_len} characters")
    return value


class UserProfileRequired(BaseModel):
    name: str
    address: str
    city: str
    country: str
    trade_licensing_office: str
    ico: str
    dic: str
    email: str
    phone: str
    bank: str
    iban: str
    swift: str

    @field_validator(
        "name",
        "address",
        "city",
        "country",
        "trade_licensing_office",
        "ico",
        "dic",
        "email",
        "phone",
        "bank",
        "iban",
        "swift",
        mode="before",
    )
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
        return _validate_length(value, MAX_NAME_LENGTH, "Name")

    @field_validator("address")
    @classmethod
    def validate_address_length(cls, value: str) -> str:
        return _validate_length(value, MAX_ADDRESS_LENGTH, "Address")

    @field_validator("city")
    @classmethod
    def validate_city_length(cls, value: str) -> str:
        return _validate_length(value, MAX_CITY_LENGTH, "City")

    @field_validator("country")
    @classmethod
    def validate_country_length(cls, value: str) -> str:
        return _validate_length(value, MAX_COUNTRY_LENGTH, "Country")

    @field_validator("trade_licensing_office")
    @classmethod
    def validate_trade_licensing_office_length(cls, value: str) -> str:
        return _validate_length(
            value, MAX_TRADE_LICENSING_OFFICE_LENGTH, "Trade licensing office"
        )

    @field_validator("email")
    @classmethod
    def validate_email_length(cls, value: str) -> str:
        return _validate_length(value, MAX_EMAIL_LENGTH, "Email")

    @field_validator("phone")
    @classmethod
    def validate_phone_length(cls, value: str) -> str:
        return _validate_length(value, MAX_PHONE_LENGTH, "Phone")

    @field_validator("bank")
    @classmethod
    def validate_bank_length(cls, value: str) -> str:
        return _validate_length(value, MAX_BANK_LENGTH, "Bank")

    @field_validator("iban")
    @classmethod
    def validate_iban_length(cls, value: str) -> str:
        return _validate_length(value, MAX_IBAN_LENGTH, "IBAN")

    @field_validator("swift")
    @classmethod
    def validate_swift_length(cls, value: str) -> str:
        return _validate_length(value, MAX_SWIFT_LENGTH, "SWIFT")

    @field_validator("ico")
    @classmethod
    def validate_ico_length(cls, value: str) -> str:
        return _validate_length(value, MAX_ICO_LENGTH, "ICO")

    @field_validator("dic")
    @classmethod
    def validate_dic_length(cls, value: str) -> str:
        return _validate_length(value, MAX_DIC_LENGTH, "DIC")


class UserUpsert(UserProfileRequired):
    pass


class UserOut(BaseModel):
    id: str
    name: str | None
    address: str | None
    city: str | None
    country: str | None
    trade_licensing_office: str | None
    ico: str | None
    dic: str | None
    email: str | None
    phone: str | None
    bank: str | None
    iban: str | None
    swift: str | None
    created_at: str
    updated_at: str
