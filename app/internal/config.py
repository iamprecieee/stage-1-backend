from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    allowed_origins: str
    allowed_hosts: str
    use_middleware: str
    numbers_api_timeout: int = Field(default=5)
    numbers_api_base_url: str = Field(default="http://numbersapi.com")
    cache_expiry: int = Field(default=300)
    cache_max_size: int = Field(default=100)
    
    model_config = SettingsConfigDict(env_file=".env")
    
    
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()