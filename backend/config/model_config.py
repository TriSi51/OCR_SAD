import os
from dotenv import load_dotenv

load_dotenv()

def load_api_key():
    if os.getenv('LLM_NAME') == "gemini":
        api_key = os.getenv('GEMINI_API_KEY')
    
    return api_key

