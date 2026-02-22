#Запуск FastAPI, подключение роутеров

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
# Импорт настроек базы, моделей и схем из ваших соседних файлов
from .database import get_db, engine, Base
from .models import Item
from .schemas import ItemCreate, ItemResponse

app = FastAPI()

# Событие запуска приложения
@app.on_event("startup")
async def startup():
    # Создает все таблицы в БД, которые унаследованы от Base
    async with engine.begin() as conn:
        # Выполняет синхронную команду создания таблиц в асинхронном контексте
        await conn.run_sync(Base.metadata.create_all)

# Эндпоинт для создания записи
@app.post("/items/", response_model=ItemResponse)
async def create_item(item_data: ItemCreate, db: AsyncSession = Depends(get_db)):
    # Распаковывает Pydantic-схему в аргументы модели SQLAlchemy
    new_item = Item(**item_data.model_dump())
    db.add(new_item)         # Добавляет объект в сессию
    await db.commit()        # Сохраняет изменения в базу
    await db.refresh(new_item) # Подгружает созданный ID и другие поля из БД
    return new_item

# Эндпоинт для получения записи по ID
@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    # Формирует SQL: SELECT * FROM items WHERE id = :item_id
    result = await db.execute(select(Item).where(Item.id == item_id))
    # Извлекает один результат или возвращает None
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Эндпоинт для удаления
@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    # Сначала ищем объект в базе
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item:
        await db.delete(item) # Помечает объект на удаление
        await db.commit()      # Фиксирует удаление в БД
