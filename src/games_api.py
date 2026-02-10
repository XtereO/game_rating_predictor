from dotenv import load_dotenv
import os
from request_instance import RequestInstance
from datetime import datetime, timedelta

load_dotenv()

base_url = "https://api.rawg.io/api/"
API_KEY = os.getenv('API_KEY')

class RAWGamesAPI(RequestInstance):
    def __init__(self):
        super().__init__(base_url)
    
    def get_games_list_last_year(self, page=1):
        today = datetime.today()
        days_in_year = 365
        one_year_before = today - timedelta(days=days_in_year)
        two_years_before = today - timedelta(days=2*days_in_year)
        return self.get_games_list(two_years_before, one_year_before, page)

    def get_games_list_current_year(self, page=1):
        today = datetime.today()
        days_in_year = 365
        one_year_before = today - timedelta(days=days_in_year)
        return self.get_games_list(one_year_before, today, page)

    def get_games_list(self, date_since, date_to, page=1):
        y_s = date_since.year
        m_s = date_since.month
        y_t = date_to.year
        m_t = date_to.month
        return self.get("/games", {"dates": f"{y_s}-{m_s:02d}-01,{y_t}-{m_t:02d}-01", "page_size": 40, "page": page})
    
    def get(self, subdomain, query, params=None):
        return super().get(subdomain, self._inject_api_key(query), params)
    
    def post(self, subdomain, query={}, params=None, json_body=None):
        return super().post(subdomain, self._inject_api_key(query), params, json_body)
    
    def _inject_api_key(self, query):
        api_key_injected_query = {"key": API_KEY}
        api_key_injected_query.update(query)
        return api_key_injected_query
