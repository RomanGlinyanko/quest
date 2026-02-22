#Схемы данных (Pydantic DTO)

# Импорт базового класса для создания схем валидации
from pydantic import BaseModel

# Базовая схема: общие поля для создания и чтения
class ItemBase(BaseModel):
    title: str               # Обязательное строковое поле
    description: str | None = None  # Необязательное поле, по умолчанию None

# Схема для создания (POST-запрос)
# Наследует всё от ItemBase. Используется, чтобы клиент не присылал 'id' вручную
class ItemCreate(ItemBase):
    pass

# Схема для ответа (Response)
# Клиент должен получить и данные, и сгенерированный базой ID
class ItemResponse(ItemBase):
    id: int                  # Добавляем ID к списку полей

    # Настройка для совместимости с ORM (SQLAlchemy)
    class Config:
        # Позволяет Pydantic читать данные прямо из объектов SQLAlchemy 
        # (например, обращаться к item.title вместо item["title"])
        from_attributes = True 
