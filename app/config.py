import os

from dotenv import load_dotenv


load_dotenv()


def _database_url():
    url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/hotel_reservation",
    )
    # Some hosting providers still expose the deprecated postgres:// scheme.
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    return url


class Config:
    """Base application configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = _database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
