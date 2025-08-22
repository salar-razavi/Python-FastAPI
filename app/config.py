from pydantic_settings import BaseSettings


class Setting (BaseSettings):
    username: str
    password: str
    host: str
    port: int
    database: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    class Config:
        env_file=".env"


setting = Setting()