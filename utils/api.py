
import discord
import logging
import random
import requests

from config.config import (
    API_TOKI_ACTIVITIES_URL,
    API_TOKI_ACTIVITIES_PARAMS,
    API_TOKI_ACTIVITIES_HEADERS,
)


class Club9API():
    """
    This class provides methods to fetch data from APIs using HTTP requests in order to query live activities for the Club9 fan reward program known as Club9.
    """
    def __init__(self, logger: logging.Logger):
        """
        Initializes the Club9 API client.
        """
        self.logger = logger


    def fetch(self, url: str | bytes, params: dict = None, headers: dict = None) -> dict:
        """
        Fetches data from the given API URL.

        @param url: The HTTPS URL of the API.
        @param params: Query string parameters to include in the request.
        @param headers: HTTP headers to add to the request.
        @return A JSON dictionary if successful, otherwise None.
        """
        try:
            response = requests.get(url=url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.log(level=logging.ERROR, msg=f"Club9API -> failed to fetch data for query with url = {url}, params = {params}, headers = {headers} ({e})")
            return None


    def fetch_activities(self) -> dict:
        """
        Fetches activities data from the Club9 TOKI API.

        This method calls the fetch method using the url, params, and headers loaded from config.py to retrieve a dict of all live activities. If the fetch is unsuccessful, the output of this method is None.

        @return: A JSON dictionary if successful, otherwise None.
        """
        url = API_TOKI_ACTIVITIES_URL
        params = API_TOKI_ACTIVITIES_PARAMS
        headers = API_TOKI_ACTIVITIES_HEADERS
        self.logger.log(level=logging.INFO, msg=f"Club9API -> fetching activities")
        activities = self.fetch(url=url, params=params, headers=headers)
        return activities
