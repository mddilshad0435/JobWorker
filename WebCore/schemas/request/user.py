from pydantic import BaseModel, EmailStr, Field
from typing import Union, Optional


class UserSignupSchema(BaseModel):
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    email: EmailStr = Field()
    password: str = Field()
    username: str = Field()   # because username==email
    confirm_password: str = Field()
    role_id: int = Field(default=3)

class UserLoginSchema(BaseModel):
    email: EmailStr = Field()
    password: str = Field()


class UserResetSchema(BaseModel):
    email: EmailStr = Field(default=None)
    old_password: str = Field()
    new_password: str = Field()

class UserModel(BaseModel):
    name : str
    email : str
    password : str

class TokenData(BaseModel):
    email: Union[str, None] = None

class UserDetails(BaseModel):
    email : str = Field()
    first_name: str = Field()
    last_name: str = Field(default=None)
    mobile: int = Field(default=None)
    bio: str = Field(default=None)


class userAddressSchema(BaseModel):
    country_id: int = Field()
    state_id: int = Field(default=None)
    city_id: int = Field()
    zip : int = Field()
    address: str = Field()
    address2: str = Field(default=None)
