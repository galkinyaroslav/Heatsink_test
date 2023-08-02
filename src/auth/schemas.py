from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, BaseModel, validator


# class ModelNaiveDt(BaseModel):
#     dt: datetime = None
#
#     @validator("dt", pre=True)
#     def dt_validate(cls, dt):
#         return datetime.fromtimestamp(dt)


class UserRead(schemas.BaseUser[int]):
    username: str
    email: EmailStr
    role_id: int
    registered_datetime: datetime  # return after register
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    role_id: int
    # registered_datetime: datetime  # uses in body query, not need manually entering
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    email: EmailStr
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
