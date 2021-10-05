from typing import Optional

from pydantic import BaseModel


class PermissionSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    email: str
    permissions: list[PermissionSchema]

    class Config:
        orm_mode = True


class UserCreateSchema(UserSchema):
    permissions: set[str]
    password: str


class UserEditSchema(BaseModel):
    email: Optional[str]
    permissions: Optional[set[str]]
    password: Optional[str]


class UserResponseSchema(UserSchema):
    id: int
