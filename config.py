import os
from dotenv import load_dotenv


load_dotenv()


class Config:   
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        "postgresql://user:password@localhost:5432/app_db"
    )
