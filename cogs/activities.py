
from discord.ext import commands
import json
import logging

from config.config import *
from main import Club9Bot
import utils.activity


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
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Activities -> reading activities cache")
            with open(PATH_TOKI_ACTIVITIES_CACHE, "r") as file:
                self.club9_bot.activities_dict = json.load(file)
            activities_list = self.club9_bot.activities_dict.get("activities", [])
            activities_data = utils.activity.generate_activities(activities_list=activities_list)
            for activity_data in activities_data:
                if (hasattr(activity_data, "id") == False or activity_data.club9_activity_type == utils.activity.Club9ActivityType.NONE):
                    continue
                else:
                    self.club9_bot.activities_mapping[activity_data.id] = activity_data
        except FileNotFoundError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activities -> failed to read activities cache (file not found)")
        except json.JSONDecodeError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activities -> failed to decode activities cache (json decode error)")
        except Exception as e:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activities -> failed to read activities cache ({e})")


    async def write_cache(self) -> None:
        """
        Write a cache file storing the current activities data.

        This method writes a JSON cache file and assigns the data from the bot's activities data attribute to the file. Upon startup, this cache is read, allowing the bot to track which activities are old compared to any new requests.
        """
        try:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Activities -> writing activities cache")
            with open(PATH_TOKI_ACTIVITIES_CACHE, "w") as file:
                json.dump(self.club9_bot.activities_dict, file, indent=4)
        except FileNotFoundError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activities -> failed to write activities cache (file not found)")
        except json.JSONDecodeError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activities -> failed to decode activities cache (json decode error)")
        except Exception as e:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activities -> failed to write activities cache ({e})")


    async def refresh(self) -> None:
        """
        Refreshes the bot's activities to determine whether any activities have been added/removed/modified.

        This method queries the TOKI API and compares the requested data with the previous activities to detect changes. If changes are detected, the method will determine the exact changes and follow the corresponding logic; i.e., send or modify a notification, write to the activities cache.
        """
        try:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Activities -> refreshing activities")
            activities_dict: dict = self.club9_bot.api.fetch_activities()
            if (activities_dict == self.club9_bot.activities_dict):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Activities -> refreshed activities (no changes detected)")
            else:
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Activities -> refreshed activities (changes detected)")
                activities_list = activities_dict.get("activities", [])
                activities_data = utils.activity.generate_activities(activities_list=activities_list)
                for activity_data_new in activities_data:
                    if (hasattr(activity_data_new, "id") == False or activity_data_new.club9_activity_type == utils.activity.Club9ActivityType.NONE):
                        # TODO log skip?
                        continue
                    else:
                        activity_data_old: utils.activity.Club9ActivityData = self.club9_bot.activities_mapping.get(activity_data_new.id, utils.activity.Club9ActivityData(data={}))        # default value is empty activity (need comparison for new activities since key wouldn't exist in mapping)
                        if (activity_data_old.club9_activity_data == activity_data_new.club9_activity_data):
                            # TODO CASE 1 -> detected constant current activity
                            # print("no change")
                            pass
                        else:
                            # TODO CASE 2 -> detected added/modified current activity
                            content = activity_data_new.generate_activities_content()
                            embed = activity_data_new.generate_activities_embed()
                            await self.club9_bot.club9_cog_notifications.send_notification(channel_id=DISCORD_CHANNEL_ID_CLUB9_NOTIFICATIONS, content=content, embed=embed)
        except Exception as e:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Activities -> failed to refresh activities ({e})")


async def setup(bot: Club9Bot) -> None:
    """
    Adds the cog to the discord bot during extension load.
    """
    await bot.add_cog(Club9Activities(bot))
