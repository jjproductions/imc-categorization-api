from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_IOM_USER: str
    db_iom_password: str
    DB_IOM_DATABASE: str = 'IOM_CC'
    DB_SERVER: str = 'localhost'
    SECRET_KEY: str
    algorithm: str = 'HS256'
    access_token_expire_min:int = 30

settings = Settings()