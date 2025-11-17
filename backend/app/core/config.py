from pydantic import BaseModel
import os, json

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@db:5432/emissions")
    api_cors_origins: list[str] = json.loads(os.getenv("API_CORS_ORIGINS", "[\"http://localhost:5173\"]"))

settings = Settings()
