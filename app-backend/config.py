from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://postgres:693593@localhost:5432/Kiosco_eventos"
    debug: bool = True
    cors_allowed_origins: list[str] = ["*"]

settings = Settings()