import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure necessary environment variables are set
REQUIRED_ENV_VARS  = ['DATABASE_URI', 'SECRET_KEY', 'FLASK_ENV']
missing_env_vars = [var for var in REQUIRED_ENV_VARS  if not os.getenv(var)]
if missing_env_vars:
    raise EnvironmentError(f"Required environment variables are missing: {', '.join(missing_env_vars)}")

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = True if os.getenv('FLASK_ENV') == 'development' else False
