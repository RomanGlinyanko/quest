from datetime import datetime
from typing import List, Optional
# Импортируем типы данных, которые понимает PostgreSQL
from sqlalchemy import BigInteger, ForeignKey, Text, DateTime, UniqueConstraint, func
# Импортируем инструменты для маппинга классов на таблицы
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# 1. Создаем фундамент. Все ваши модели должны наследоваться от этого класса.
# Он регистрирует все таблицы в метаданных SQLAlchemy.
class Base(DeclarativeBase):
    pass

# --- Таблица Пользователи ---
class User(Base):
    __tablename__ = "users" # Имя таблицы в точности как в вашем SQL-скрипте
    
    # Mapped[int] — это аннотация для Python (тайп-хинтинг).
    # mapped_column — это описание колонки для БД.
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    # nullable=False соответствует вашему ограничению NOT NULL
    email: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Optional[str] означает, что в коде поле может быть None
    # unique=True автоматически создаст индекс (как мы обсуждали)
    login: Mapped[Optional[str]] = mapped_column(Text, unique=True)
    
    # server_default=func.current_timestamp() перекладывает генерацию времени на PostgreSQL.
    # Это "идеально", так как время будет точным, даже если на сервере с Python оно сбито.
    insert_ts: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=func.current_timestamp()
    )

    # Виртуальная связь (не колонка в БД!). 
    # Позволяет писать user.questions и получать список всех его вопросов.
    questions: Mapped[List["Quest"]] = relationship(back_populates="author")

# --- Таблица Соединение Пространства - Вопрос ---
class ConnSpaceQuest(Base):
    __tablename__ = "conn_space_quest"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    # ForeignKey указывает на связь. ondelete="CASCADE" критически важен:
    # если удалить тему, связь удалится автоматически.
    space_id: Mapped[int] = mapped_column(
        ForeignKey("quest_space.id", ondelete="CASCADE"), 
        nullable=False
    )
    quest_id: Mapped[int] = mapped_column(
        ForeignKey("quest.id", ondelete="CASCADE"), 
        nullable=False
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    
    # __table_args__ используется для описания индексов и ограничений на уровне всей таблицы.
    # Здесь мы жестко фиксируем составной уникальный ключ (space_id + quest_id).
    __table_args__ = (
        UniqueConstraint("space_id", "quest_id", name="uq_space_quest"),
    )

# --- Таблица Вопросы ---
class Quest(Base):
    __tablename__ = "quest"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    quest: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    
    # Обратная сторона связи с User. 
    # Позволяет для любого вопроса быстро узнать автора: my_quest.author.login
    author: Mapped["User"] = relationship(back_populates="questions")
    
    # Добавим связь Many-to-Many к терминам через таблицу conn_quest_term
    terms: Mapped[List["TermDict"]] = relationship(
        secondary="conn_quest_term", 
        back_populates="questions"
    )

# --- Таблица Словарь терминов ---
class TermDict(Base):
    __tablename__ = "term_dict"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    term: Mapped[str] = mapped_column(Text, nullable=False)
    definition: Mapped[str] = mapped_column(Text, name="def") # name="def", т.к. def - зарезервировано в Python
    comment: Mapped[Optional[str]] = mapped_column(Text, name="comm")
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    
    # Позволяет найти все вопросы, где упоминается этот термин
    questions: Mapped[List["Quest"]] = relationship(
        secondary="conn_quest_term", 
        back_populates="terms"
    )
