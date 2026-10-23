import re
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import status

from app.db.models import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.security import hash_password, verify_password, dummy_verify_password, create_access_token
from app.core.errors import AppException
from app.core.config import settings

class AuthService:
    @staticmethod
    async def register(db: AsyncSession, payload: RegisterRequest) -> dict:
        # Check password criteria: min 8 char, at least 1 letter and 1 digit
        has_letter = bool(re.search(r'[A-Za-z]', payload.password))
        has_digit = bool(re.search(r'\d', payload.password))
        password_format_valid = len(payload.password) >= 8 and has_letter and has_digit
        password_match = payload.password == payload.password_confirmation

        if not password_match or not password_format_valid:
            error_field = "password_confirmation" if not password_match else "password"
            error_msg = "Konfirmasi sandi tidak cocok" if not password_match else "Sandi harus memuat minimal 8 karakter dengan huruf dan angka"
            raise AppException(
                message="Format sandi tidak valid atau konfirmasi sandi tidak cocok",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                error_code="INVALID_PASSWORD",
                errors=[{"field": error_field, "message": error_msg}]
            )

        # Check existing user
        stmt = select(User).where(User.alamat_email == payload.email)
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise AppException(
                message="Email sudah terdaftar",
                status_code=status.HTTP_409_CONFLICT,
                error_code="EMAIL_TAKEN"
            )

        hashed = hash_password(payload.password)
        now = datetime.now(timezone.utc)
        new_user = User(
            nama_lengkap=payload.name,
            alamat_email=payload.email,
            password=hashed,
            tanggal_registrasi=now
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return {
            "id_user": new_user.id_user,
            "name": new_user.nama_lengkap,
            "email": new_user.alamat_email,
            "tanggal_registrasi": new_user.tanggal_registrasi.isoformat() if new_user.tanggal_registrasi else now.isoformat()
        }

    @staticmethod
    async def login(db: AsyncSession, payload: LoginRequest) -> dict:
        stmt = select(User).where(User.alamat_email == payload.email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            # Timing defense
            dummy_verify_password(payload.password)
            raise AppException(
                message="Kredensial tidak valid",
                status_code=status.HTTP_401_UNAUTHORIZED,
                error_code="INVALID_CREDENTIALS"
            )

        if not verify_password(payload.password, user.password):
            raise AppException(
                message="Kredensial tidak valid",
                status_code=status.HTTP_401_UNAUTHORIZED,
                error_code="INVALID_CREDENTIALS"
            )

        expires_in = settings.JWT_EXPIRE_HOURS * 3600
        token = create_access_token({
            "sub": str(user.id_user),
            "email": user.alamat_email
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": expires_in,
            "user": {
                "id_user": user.id_user,
                "name": user.nama_lengkap,
                "email": user.alamat_email
            }
        }
