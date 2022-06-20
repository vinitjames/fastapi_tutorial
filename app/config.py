from pydantic import BaseSettings

class DatabaseSettings(BaseSettings):
    postgres_username: str
    postgres_hostname: str
    postgres_port: int
    postgres_password: str
    postgres_dbname: str

    class Config:
        env_file = ".env"


class OAUTH2Settings(BaseSettings):
    JWT_secret_key: str
    JWT_algorithm: str
    JWT_timeout: int
    
    class Config:
        env_file = ".env"
        
db_config = DatabaseSettings()
oauth2_config = OAUTH2Settings()
    
