import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SQLALCHEMY_SECRET_KEY = os.environ.get("SQLALCHEMY_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    OPEN_AI_SECRET_KEY = os.environ.get("OPEN_AI_SECRET_KEY")
    SECRET_KEY = os.environ.get('SECRET_KEY')
    NOMIC_API_KEY = os.environ.get('NOMIC_API_KEY')
    # Add more configuration parameters as needed
