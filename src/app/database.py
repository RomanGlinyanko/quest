import asyncio
from typing import AsyncGenerator

# Импортируем асинхронные инструменты SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# Импортируем базовый класс из вашего models.py (чтобы знать о таблицах)
from .models import Base 

# 1. URL подключения. 
# Формат: postgresql+asyncpg://логин:пароль@хост:порт/имя_базы
# В идеале это должно браться из переменных окружения (.env)
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/exam_trainer"

# 2. Создаем Engine — это "мотор", который умеет общаться с БД.
# echo=True заставит алхимию печатать все SQL-запросы в консоль (полезно при отладке)
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True # Использовать API SQLAlchemy 2.0
)

# 3. Создаем фабрику сессий. 
# expire_on_commit=False критично для асинхронности, чтобы объекты не "пропадали" после коммита.
async_session_maker = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 4. Dependency для FastAPI (или другого веб-фреймворка).
# Этот генератор будет выдавать сессию на каждый запрос и автоматически закрывать её.
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# 5. Вспомогательная функция для инициализации таблиц (если их еще нет).
# В реальных проектах лучше использовать миграции (Alembic), 
# но для старта это полезно.
async def init_db():
    async with engine.begin() as conn:
        # Это создаст все таблицы, описанные в models.py
        # Внимание: если таблицы уже есть в БД, он их не тронет.
        await conn.run_sync(Base.metadata.create_all)