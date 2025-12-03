"""
Environment variable utilities
"""
import os
from pathlib import Path
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)

def get_required_env(key: str) -> str:
    """Get required environment variable or raise error"""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Required environment variable {key} is not set")
    return value

def get_optional_env(key: str, default: str = "") -> str:
    """Get optional environment variable with default"""
    return os.getenv(key, default)

# Load environment on module import
load_environment()
