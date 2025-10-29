from pydantic_settings import BaseSettings
from pydantic import SecretStr
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

class DatabaseSettings(BaseSettings):
    PG_HOST: str
    PG_PORT: int
    PG_PASSWORD: SecretStr
    PG_DATABASE: str
    PG_USERNAME: str

        
    @property
    def pg_link(self) -> URL:
        
        link = URL.create(
            drivername = "postgresql+asyncpg",
            username = self.PG_USERNAME,
            password = self.PG_PASSWORD.get_secret_value(),
            host = self.PG_HOST,
            port = self.PG_PORT,
            database = self.PG_DATABASE
        )

        return link


    class Config:
        extra = "ignore"

db_settings = DatabaseSettings()


engine = create_async_engine(
    db_settings.pg_link.render_as_string(hide_password = False),
    pool_pre_ping=True,
    pool_recycle=3600,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)

