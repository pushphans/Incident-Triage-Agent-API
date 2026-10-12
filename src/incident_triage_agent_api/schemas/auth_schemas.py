from datetime import datetime
from uuid import UUID
from pydantic import EmailStr
from pydantic import Field
from pydantic import BaseModel


class RegisterRequestModel(BaseModel):
    name : str = Field(..., max_length=100)
    email : EmailStr = Field(...)
    password : str = Field(..., min_length=6)


class RegisterResponseSchema(BaseModel):
    id : UUID
    name : str
    email : str
    created_at : datetime
    updated_at : datetime


class LoginRequestSchema(BaseModel):
    email : EmailStr = Field(...)
    password : str = Field(..., min_length=6)


class LoginResponseModel(BaseModel):
    user_id : UUID
    name : str
    email : str
    access_token : str
    access_token_expiry : int
    refresh_token : str
    created_at : datetime
    updated_at : datetime


class TokenRefreshRequestSchema(BaseModel):
    refresh_token : str


class TokenRefreshResponseSchema(BaseModel):
    refresh_token : str
    access_token : str
    access_token_expiry : int
    