import os
from dotenv import load_dotenv

load_dotenv()

COINDCX_API_KEY = os.getenv("COINDCX_API_KEY")
COINDCX_API_SECRET = os.getenv("COINDCX_API_SECRET")
COINDCX_BASE_URL = "https://api.coindcx.com"
