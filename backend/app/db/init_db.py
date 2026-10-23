from app.core.database import engine, Base
from app.db.models import User, DokumenUpload, DrafKebutuhan, AuditKebutuhan, TemuanCacat, HistoryDownload, PasswordResetToken

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
