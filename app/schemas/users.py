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
