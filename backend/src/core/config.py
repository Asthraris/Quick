from pydantic_settings import BaseSettings, SettingsConfigDict

# this class creates an instance of seeting obj which posses all our secrets fetched from .env instead of using load_end at every file just use this obj which just fecthes once
class Settings(BaseSettings):
    JWT_SECRET_KEY :str
    JWT_ALGORITHM :str
    JWT_EXPIRATION :int = 30
    DATABASE_URL:str 
#this tells the env path and what to do with extra variables 
#also the path is relative to(agar kuch bhi fect ka issue aye toh ye check karna)
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

# Instantiate it once (no need to instantiate in main.py)
settings = Settings()