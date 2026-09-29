from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    currency_api_token: str
    database_password: str
    database_port: str
    database_username: str
    database_name: str
    database_hostname: str
    admin_username: str
    admin_password: str

settings = Settings()