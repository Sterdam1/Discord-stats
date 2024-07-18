from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    
    username: str = Field('username', alias='DB_USERNAME')
    password: str = Field('password', alias='DB_PASSWORD')
    host: str = Field('host', alias='DB_HOST')
    database: str = Field('database', alias='DB_DATABASE')
    port: str = Field('port', alias="DB_PORT")

        
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    
    bot_token: str = Field('bot_token', alias='BOT_TOKEN')
    # tg_token: str = Field('tg_token', alias='TG_TOKEN')

    db: DbSettings = Field(default_factory=DbSettings)
    
settings = Settings()


# print(settings)
# print(settings.db.username)