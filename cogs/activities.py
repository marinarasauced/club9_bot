
from discord.ext import commands
from enum import Enum
import json
import logging

from config.config import *
from main import Club9Bot
from utils.api import Club9API


class Club9ActivityType(Enum):
    """
    This class provides several enum used to differentiate activity types.
    """
    QUEST_INTERNAL = 0      # Users complete the activity on the 'https://store.cloud9.gg/pages/club9' page.
    QUEST_EXTERNAL = 1      # Users complete the activity external to the 'https://store.cloud9.gg/pages/club9' page.
    CHALLENGE = 2           # Users complete the activity by completing several quests.
    NONE = 3                # A placeholder value for quests that have not yet been loaded.


class Club9Activity(commands.Cog):
    """
    This class provides a structure to map and store data from the TOKI API activity requests and asynchronous methods relating to the activities data.

    @param bot: The Club9Bot to load this cog.
    """
    def __init__(self, bot: Club9Bot):
        """
        Initializes the Club9 activity.
        """
        self.club9_bot = bot
        self.club9_activity_type = Club9ActivityType.NONE


    async def read_cache(self) -> None:
        """
        Reads a cache file storing the previous activities data.

        This method reads a JSON cache file and assigns the data to a bot attribute in order to speed up fetching. Upon refreshes, the bot first compares the cache to the new request data before proceeding to break down any added/removed/modified quests when differences are detected between the cache and the request. This method is only called on startup.
        """
        try:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Activity -> reading activities cache")
            with open(PATH_TOKI_ACTIVITIES_CACHE, "r") as file:
                self.club9_bot.activities = json.load(file)
        except FileNotFoundError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activity -> failed to read activities cache (file not found)")
        except json.JSONDecodeError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activity -> failed to decode activities cache (json decode error)")
        except Exception as e:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activity -> failed to read activities cache ({e})")


    async def write_cache(self) -> None:
        """
        Write a cache file storing the current activities data.

        This method writes a JSON cache file and assigns the data from the bot's activities data attribute to the file. Upon startup, this cache is read, allowing the bot to track which activities are old compared to any new requests.
        """
        try:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Activity -> writing activities cache")
            with open(PATH_TOKI_ACTIVITIES_CACHE, "w") as file:
                json.dump(self.club9_bot.activities, file, indent=4)
        except FileNotFoundError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activity -> failed to write activities cache (file not found)")
        except json.JSONDecodeError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activity -> failed to decode activities cache (json decode error)")
        except Exception as e:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activity -> failed to write activities cache ({e})")
