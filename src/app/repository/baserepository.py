from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Base

# Объявляем переменную типа, которая должна быть наследником нашей Base модели
T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    """
    Абстрактный базовый класс для всех репозиториев.
    Generic[T] позволяет IDE понимать, какой тип данных возвращает метод.
    """
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        """Получить одну запись по первичному ключу"""
        return await self.session.get(self.model, obj_id)

    async def get_all(self) -> List[T]:
        """Получить все записи таблицы"""
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def delete(self, obj_id: int) -> None:
        """Удалить запись по ID"""
        query = delete(self.model).filter(self.model.id == obj_id)
        await self.session.execute(query)
        # Мы не делаем commit здесь, это сделает Unit of Work или сервис
