import os
from pydantic_settings import BaseSettings

class DevelopmentConfig(BaseSettings):
    DB_IOM_DATABASE: str = 'IMC'
    DB_SERVER: str = 'jbpostgres.postgres.database.azure.com'
    algorithm: str = 'HS256'
    access_token_expire_min:int = 30

class ProductionConfig(BaseSettings):
    DB_IOM_DATABASE: str = 'IOM_CC'
    DB_SERVER: str = 'localhost'
    algorithm: str = 'HS256'
    access_token_expire_min:int = 30

def get_config():
    env = os.getenv("ENV", "development").lower()
    if env == "production":
        print("Using ProductionConfig")
        return ProductionConfig()
    else:
        print("Using DevelopmentConfig")
        return DevelopmentConfig()

print("Settings loaded:")
settings = get_config()