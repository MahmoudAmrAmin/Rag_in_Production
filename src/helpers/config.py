from pydantic_settings import BaseSettings , SettingsConfigDict
from dotenv import load_dotenv , find_dotenv


class Settings(BaseSettings) : 
    # use data validation concepts from pydentic  
    APP_NAME : str 
    APP_VERSION :str 
    # Define File Validation information 
    FILE_ALLOWED_TYPES:list 
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNK_SIZE:int
    class Config: 
        env_file = find_dotenv()  


# here we will make functi on that return object from Settings class 

def get_settings() : 
    return Settings()
         