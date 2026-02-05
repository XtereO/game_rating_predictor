from dotenv import load_dotenv
import os
import requests
from datetime import datetime

load_dotenv()

API_KEY = os.getenv('API_KEY')

today = datetime.today()
year = today.year
month = today.month

#games_data = requests.get(f"https://api.rawg.io/api/games?key={API_KEY}&dates={year-2}-{month:02d}-01,{year-1}-{month:02d}-01")
