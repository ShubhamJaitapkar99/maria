import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool

# Load environment variables from .env file
load_dotenv()

# Get API Keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RUNWAY_API_SECRET = os.getenv("RUNWAYML_API_SECRET")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
LEONARDO_API_KEY = os.getenv("LEONARDO_API_KEY")
LEONARDO_CONTENT_API_KEY = os.getenv("LEONARDO_CONTENT_API_KEY")
AKOOL_CLIENT_ID = os.getenv("AKOOL_CLIENT_ID")
AKOOL_CLIENT_SECRET = os.getenv("AKOOL_CLIENT_SECRET")

# Initialize environment variables
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["RUNWAYML_API_SECRET"] = RUNWAY_API_SECRET
os.environ["SERPER_API_KEY"] = SERPER_API_KEY

# Initialize tools
search_tool = SerperDevTool(api_key=SERPER_API_KEY)

# Session state initialization
DEFAULT_SESSION_STATE = {
    'generated_image_url': None,
    'dalle_prompt': None,
    'video_generated': False,
    'generated_content': []
}