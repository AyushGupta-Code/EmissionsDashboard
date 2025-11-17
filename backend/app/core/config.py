from pydantic import BaseModel
import os, json

class Settings(BaseModel):
    """Application level settings.

    The project primarily targets PostgreSQL (TimescaleDB) but several
    contributors run the API locally without spinning up the database.  The
    ``database_schema`` flag lets the code know whether explicit schema
    qualification (``air.stations``) should be used.  When we fall back to the
    built-in SQLite demo database the schema is set to ``None`` so the same
    queries work transparently.
    """

    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@db:5432/emissions",
    )
    database_schema: str | None = os.getenv("DATABASE_SCHEMA", "air")
    api_cors_origins: list[str] = json.loads(
        os.getenv("API_CORS_ORIGINS", "[\"http://localhost:5173\"]")
    )

settings = Settings()
