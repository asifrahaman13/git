# sample config file

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

CLIENT_ID=os.getenv('CLIENT_ID')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')
REDIRECT_URI=os.getenv('REDIRECT_URI')
GITHUB_API_URL=os.getenv('GITHUB_API_URL')
PASSWORD=os.getenv('PASSWORD')
FRONT_END_URL=os.getenv('FRONT_END_URL')

REPO_HUB=os.getenv('REPO_HUB')