from typing import Optional, List
from sqlalchemy import String, Column
from sqlmodel import SQLModel, Field, Relationship

from app.validators import PasswordValidator

#  Relationships
class UserPermissionLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    permission_id: Optional[int] = Field(
        default=None, foreign_key="permission.id", primary_key=True
    )


#  Permission
class PermissionBase(SQLModel):
    name: str = Field(sa_column=Column("name", String, unique=True), max_length=75)


class Permission(PermissionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


#  User
class UserBase(SQLModel):
    email: str = Field(sa_column=Column("email", String, unique=True), max_length=320)


class UserCreate(UserBase, PasswordValidator):
    password: str


class UserEdit(SQLModel, PasswordValidator):
    email: Optional[str]
    password: Optional[str]


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    permissions: List[Permission] = Relationship(link_model=UserPermissionLink)
    is_active: Optional[bool] = Field(default=True)


class UserRead(UserBase):
    id: int
    is_active: bool


class UserReadWithPermissions(UserRead):
    permissions: list[PermissionBase] = []
