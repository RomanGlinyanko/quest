from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """
    Класс настроек. Pydantic автоматически ищет переменные 
    с такими именами в окружении или в .env файле.
    """
    # Регистр не важен (DB_USER в .env превратится в db_user здесь)
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url_asyncpg(self) -> str:
        """Собирает строку подключения для asyncpg"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Указываем, откуда брать данные, если их нет в переменных окружения системы
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Создаем экземпляр настроек (Singleton), который будем импортировать везде
settings = Settings()
