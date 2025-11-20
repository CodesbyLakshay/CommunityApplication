from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    db_port: str
    db_hostname: str
    db_name: str
    db_username: str
    db_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()