from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    host: str = Field('def_host', alias='DB_HOST')
        
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    
    bot_token: str = Field('bot_token', alias='BOT_TOKEN')
    # tg_token: str = Field('tg_token', alias='TG_TOKEN')

    # db_settings: DbSettings = Field(default_factory=DbSettings)
    
settings = Settings()

# print(settings)
