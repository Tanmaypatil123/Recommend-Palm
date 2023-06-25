import os
import dotenv

dotenv.load_dotenv()


SESSION_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}"
}