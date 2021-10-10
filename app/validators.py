from pydantic import BaseModel, validator

from app.config import MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH


class PasswordValidator(BaseModel):
    @validator("password", check_fields=False)
    def password_validator(cls, value):
        if not value:
            return

        if len(value) > MAX_PASSWORD_LENGTH or len(value) < MIN_PASSWORD_LENGTH:
            raise ValueError(
                f"Password length must be between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH}"
            )

        return value
