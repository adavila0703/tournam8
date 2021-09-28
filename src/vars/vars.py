import os
from dotenv import load_dotenv
from enum import Enum, unique

load_dotenv()

@unique
class Env(Enum):
    API_PATH: str = os.environ.get('API_PATH')
    OCR_ENGINE_PATH: str = os.environ.get('OCR_ENGINE_PATH')
    DISCORD_TOKEN: str = os.environ.get('DISCORD_TOKEN')
    THRESHOLD_VALUE: int = int(os.environ.get('THRESHOLD_VALUE'))
    MAX_VALUE: int = int(os.environ.get('MAX_VALUE'))
    IMREAD_FLAG: int = int(os.environ.get('IMREAD_FLAG'))
    OCR_LANGUAGE: str = os.environ.get('OCR_LANGUAGE')
    OCR_CONFIG: str = os.environ.get('OCR_CONFIG')
    OCR_PROC_PRIORITY: int = int(os.environ.get('OCR_PROC_PRIORITY'))

print(type(Env.THRESHOLD_VALUE.value))