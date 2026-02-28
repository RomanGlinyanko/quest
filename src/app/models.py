#Таблицы БД (SQLAlchemy)

# Импорт инструментов для аннотации типов (Mapped) и настройки колонок (mapped_column)
from sqlalchemy.orm import Mapped, mapped_column
# Импорт базового класса Base из вашего файла database.py (где объявлен DeclarativeBase)
from .database import Base

# Объявление класса модели, который наследуется от Base
class Item(Base):
    # Имя таблицы, которая будет создана в базе данных PostgreSQL
    __tablename__ = "items"
    
    # Первичный ключ (ID): целое число, создается автоматически (Serial/Identity)
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Строковая колонка для заголовка. index=True создает индекс для быстрого поиска
    title: Mapped[str] = mapped_column(index=True)
    
    # Описание. Аннотация 'str | None' (или Optional[str]) делает колонку NULLABLE в базе
    # (то есть поле может быть пустым)
    description: Mapped[str | None]