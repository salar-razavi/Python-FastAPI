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
    username_test: str
    password_test: str
    host_test: str
    port_test: int
    database_test: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    testing: bool = False
    seed_on_startup: bool = True

setting = Setting()
