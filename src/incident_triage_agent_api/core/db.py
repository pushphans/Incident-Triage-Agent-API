from incident_triage_agent_api.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase



async_engine = create_async_engine(
    url=settings.DATABASE_URL
)



class Base(DeclarativeBase):
    pass


session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)



async def get_db():
    async with session_factory() as db:
        yield db