from pydantic_settings import BaseSettings, SettingsConfigDict


class TokenSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TOKEN_TYPE: str = "Bearer"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="JWT_", extra="ignore")


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_NAME: str

    token: TokenSettings = TokenSettings()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")



settings = Settings()
