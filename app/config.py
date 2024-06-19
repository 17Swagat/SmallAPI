# rough:
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database:
    DATABASE_NAME: str
    DATABASE_HOST_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: str

    # Auth:
    SECRET_KEY: str # <Json-Webtoken>
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = '.env'


settings = Settings()