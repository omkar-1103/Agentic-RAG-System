import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Example configuration settings
class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    # Add other global settings here
    MAX_RETRIES = 3

config = Config()
