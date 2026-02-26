#Настройка SQLAlchemy и движка БД

# Импорт необходимых инструментов для асинхронной работы
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# Базовый класс для объявления моделей (в стиле SQLAlchemy 2.0)
from sqlalchemy.orm import DeclarativeBase

# URL подключения: используется драйвер asyncpg для асинхронной работы с Postgres
DATABASE_URL = "postgresql+asyncpg://postgres:RX777ngS@localhost/quest"

# Создание "движка" — объекта, который управляет пулом соединений с БД
engine = create_async_engine(DATABASE_URL)

# Фабрика сессий: создает объекты AsyncSession для выполнения запросов
# expire_on_commit=False предотвращает ошибку при обращении к атрибутам объекта после commit
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Создание базового класса, от которого будут наследоваться все модели (таблицы)
class Base(DeclarativeBase):
    pass

# Асинхронный генератор (Dependency Injection) для FastAPI
async def get_db():
    # Открывает сессию в контекстном менеджере (гарантирует закрытие после использования)
    async with async_session() as session:
        yield session # Возвращает сессию в обработчик запроса