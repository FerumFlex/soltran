from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = Field(env="debug", default=True)

    sentry_dsn: str = Field(env="sentry_dsn", default="")
    sentry_sample_rate: float = Field(env="sentry_sample_rate", default=0.05)
    environment: str = Field(env="environment", default="local")
    version: str = Field(env="version", default="local")
    microservice: str = Field(env="microservice", default="web")

    telegram_token: str = Field(env="telegram_token", default="")

    openai_api_key: str = Field(env="openai_api_key", default="")
    langchain_api_key: str = Field(env="langchain_api_key", default="")

    solana_endpoint_url: str = Field(env="solana_endpoint_url", default="https://api.mainnet-beta.solana.com")



settings = Settings()
