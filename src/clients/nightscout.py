import httpx

from src.utils.config import get_config
from src.utils.trend import Trend


class NightscoutClient:
    def __init__(self, http_client: httpx.Client):
        self.http_client = http_client

    def get_latest_entry(self) -> tuple[int, Trend]:
        response = self.http_client.get(
            f"{get_config().get('nightscout', 'base_url')}/api/v1/entries/sgv.json?count=1"
        )
        data = response.json()
        return (data[0].get("sgv"), Trend(data[0].get("direction")))
