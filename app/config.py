from pydantic_settings import BaseSettings ,SettingsConfigDict


class Setting (BaseSettings):
    username: str
    password: str
    host: str
    port: int
    database: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    


setting = Setting()