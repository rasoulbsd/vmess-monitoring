import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the VMess monitoring server"""
    
    # Server Configuration
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVER_PORT = int(os.getenv('SERVER_PORT', 8000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Authentication
    API_KEY = os.getenv('API_KEY', 'your-secret-api-key-here')
    USERNAME = os.getenv('USERNAME', 'admin')
    PASSWORD = os.getenv('PASSWORD', 'your-secure-password-here')
    
    # VMess Testing Configuration
    VMESSPING_BIN = os.getenv('VMESSPING_BIN', './vmessping')
    MAX_PING = int(os.getenv('MAX_PING', 5))
    INTERVAL = int(os.getenv('INTERVAL', 2))
    DEFAULT_DEST_URL = os.getenv(
        'DEFAULT_DEST_URL', 
        'https://www.gstatic.com/generate_204'
    ) 