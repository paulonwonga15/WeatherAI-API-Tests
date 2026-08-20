import os

import requests
from dotenv import load_dotenv


load_dotenv()


class WeatherAIClient:
    BASE_URL = "https://api.weather-ai.co"

    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")

        if not self.api_key:
            raise ValueError("WEATHER_API_KEY is not set in the .env file")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    def get_weather(self, lat=None, lon=None, **params):
        request_params = {
            **params
        }

        if lat is not None:
            request_params["lat"] = lat

        if lon is not None:
            request_params["lon"] = lon

        response = requests.get(
            f"{self.BASE_URL}/v1/weather",
            headers=self.headers,
            params=request_params,
            timeout=10
        )

        return response