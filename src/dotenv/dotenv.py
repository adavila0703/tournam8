from dotenv import load_dotenv
import os

load_dotenv()

ENV = {
    'API_PATH': os.environ.get('API_PATH'),
    'OCR_ENGINE_PATH': os.environ.get('OCR_ENGINE_PATH'),
    'DISCORD_TOKEN': os.environ.get('DISCORD_TOKEN')
}