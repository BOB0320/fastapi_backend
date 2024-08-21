from src.config import dbsettings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(
    "postgresql+asyncpg://neondb_owner:XKriQqRP5AI9@ep-purple-voice-a5a158vv.us-east-2.aws.neon.tech/neondb",
    echo=False,
    future=True,
    pool_size=max(5, 10),
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()