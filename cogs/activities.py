
from discord.ext import commands
import json
import logging

from config.config import *
from main import Club9Bot
from utils.activity import Club9ActivityType
from utils.api import Club9API


class Club9Activities(commands.Cog):
    """
    This class provides a structure to map and store data from the TOKI API activity requests and asynchronous methods relating to the activities data.

    @param bot: The Club9Bot to load this cog.
    """
    def __init__(self, bot: Club9Bot):
        """
        Initializes the Club9 activities cog.
        """
        self.club9_bot = bot


    async def read_cache(self) -> None:
        """
        Reads a cache file storing the previous activities data.

        This method reads a JSON cache file and assigns the data to a bot attribute in order to speed up fetching. Upon refreshes, the bot first compares the cache to the new request data before proceeding to break down any added/removed/modified quests when differences are detected between the cache and the request. This method is only called on startup.
        """
        try:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Activity -> reading activities cache")
            with open(PATH_TOKI_ACTIVITIES_CACHE, "r") as file:
                self.club9_bot.activities_data = json.load(file)
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
                json.dump(self.club9_bot.activities_data, file, indent=4)
        except FileNotFoundError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activity -> failed to write activities cache (file not found)")
        except json.JSONDecodeError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activity -> failed to decode activities cache (json decode error)")
        except Exception as e:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activity -> failed to write activities cache ({e})")


    async def refresh(self) -> None:
        """
        Refreshes the bot's activities to determine whether any activities have been added/removed/modified.

        This method queries the TOKI API and compares the requested data with the previous activities to detect changes. If changes are detected, the method will determine the exact changes and follow the corresponding logic; i.e., send or modify a notification, write to the activities cache.
        """
        try:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Activity -> refreshing activities")
            activities = self.club9_bot.api.fetch_activities()
            if (activities == self.club9_bot.activities_data):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Activity -> refreshed activities (no changes detected)")
            else:
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Activity -> refreshed activities (changes detected)")
                # TODO add logic for change detection
        except Exception as e:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activity -> failed to refresh activities ({e})")


async def setup(bot: Club9Bot) -> None:
    """
    Adds the cog to the discord bot during extension load.
    """
    await bot.add_cog(Club9Activities(bot))
