import json
from pydantic import BaseSettings
from decouple import config

class Settings(BaseSettings):
    FONTS = json.loads(config('FONTS'))
    
    
settings = Settings()