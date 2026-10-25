from fastapi import Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.core.database import get_db
from app.core.security import decode_access_token
from app.core.errors import AppException
from app.db.models import User

async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> User:
    unauthorized_exc = AppException(
        message="Sesi tidak valid atau telah berakhir",
        status_code=status.HTTP_401_UNAUTHORIZED,
        error_code="UNAUTHORIZED"
    )

    if not authorization or not authorization.startswith("Bearer "):
        raise unauthorized_exc

    token = authorization.split(" ")[1].strip()
    payload = decode_access_token(token)
    if not payload:
        raise unauthorized_exc

    sub = payload.get("sub")
    if not sub:
        raise unauthorized_exc

    try:
        user_id = int(sub)
    except (ValueError, TypeError):
        raise unauthorized_exc

    stmt = select(User).where(User.id_user == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise unauthorized_exc

    return user
