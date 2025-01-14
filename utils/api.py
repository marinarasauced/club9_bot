
import discord
import logging
import random
import requests

from config.config import (
    API_TOKI_ACTIVITIES_URL,
    API_TOKI_ACTIVITIES_PARAMS,
    API_TOKI_ACTIVITIES_HEADERS,
    DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS,
)
from utils.activities import (
    Club9ActivityType,
    Club9Activity,
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


    def fetch(self, url: str | bytes, params: dict = None, headers: dict = None):
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
            self.logger.log(level=logging.ERROR, msg=f"Club9API -> {e}")
            return None


    def get_activities(self):
        """
        Gets activities data from the Club9 TOKI API.

        This method calls the fetch method using the url, params, and headers loaded from config.py to retrieve a dict of all live activities. If the fetch is unsuccessful, the output of this method is None.

        @return: A JSON dictionary if successful, otherwise None.
        """
        url = API_TOKI_ACTIVITIES_URL
        params = API_TOKI_ACTIVITIES_PARAMS
        headers = API_TOKI_ACTIVITIES_HEADERS
        self.logger.log(level=logging.INFO, msg=f"Club9API -> fetching activities")
        activities = self.fetch(url=url, params=params, headers=headers)
        return activities


    def generate_activities_content(self):
        """
        Generates the text component of the discord notification for a new activity including a role ping and a short indication that there is a new quest/challenge.

        @return: The 'content' string for the discord bot to publish in the notification message.
        """
        messages = [
            f"<@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>, a new quest has been posted!",
            f"<@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>, a fresh quest is now live!",
            f"A new quest has arrived <@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>!",
            f"<@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>, a brand new quest is now available!",
            f"<@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>, a new quest has been added!",
            f"New quest alert <@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>!",
        ]
        content = random.choice(messages)
        return content


    def generate_activities_embed(self, activity: Club9Activity):
        """
        Generates the discord embed of the discord notification for a new activity including a name, reward, image, visibility, start/stop times if applicable, etc.
        """
        type = activity.club9_activity_type
        embed = discord.Embed(color=discord.Color.blue())
        if type == Club9ActivityType.QUEST_INTERNAL:
            pass
        elif type == Club9ActivityType.QUEST_EXTERNAL:
            pass
        elif type == Club9ActivityType.CHALLENGE:
            pass
        elif type == Club9ActivityType.NONE:
            pass
        else:
            pass
        return embed