from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# Импортируем наш конфиг
from .config import settings 

# Используем вычисляемое свойство из конфига
DATABASE_URL = settings.database_url_asyncpg

engine = create_async_engine(
    DATABASE_URL,
    echo=True, # Включаем логирование SQL в консоль
)

async_session_maker = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)