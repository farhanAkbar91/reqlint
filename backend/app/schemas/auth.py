import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirmation: str

    @field_validator("email")
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        stripped = v.strip()
        if len(stripped) < 2:
            raise ValueError("Nama minimal 2 karakter")
        return stripped

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

class UserResponse(BaseModel):
    id_user: int
    name: str
    email: str
    tanggal_registrasi: Optional[str] = None

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    password: str = Field(..., min_length=8)
    password_confirmation: str
