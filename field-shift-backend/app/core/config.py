from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://fieldshift:fieldshift@localhost:5432/fieldshift"
    cors_origins: list[str] = ["http://localhost:5173"]
    nasa_power_base_url: str = "https://power.larc.nasa.gov/api"
    use_mock_climate: bool = False


settings = Settings()
