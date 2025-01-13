
from config.config import *
from discord.ext import commands
import json
import logging
from main import Club9Bot
from utils.api_client import APIClient


class APIActivities(commands.Cog):
    """
    """
    def __init__(self, bot: Club9Bot):
        """
        """
        self.bot = bot


    async def read_api_activities_cache(self) -> None:
        """
        """
        try:
            self.bot.logger.log(level=logging.INFO, msg=f"reading api activities from cache")
            with open(PATH_CACHE_API_ACTIVITIES, "r") as file:
                self.bot.activities = json.load(file)
        except FileNotFoundError:
            self.bot.logger.log(level=logging.INFO, msg=f"failed to read api activities from cache (file not found)")
        except json.JSONDecodeError:
            self.bot.logger.log(level=logging.INFO, msg=f"failed to read api activities from cache (json decode error)")
        except Exception as e:
            self.bot.logger.log(level=logging.INFO, msg=f"failed to read api activities from cache ({e})")


    async def write_api_activities_cache(self, activities: dict[str, APIClient.Activity]) -> None:
        """
        """
        data = {}
        keys = activities.keys()
        for key in keys:
            value = activities[key].data
            data[key] = value
        self.bot.logger.log(level=logging.INFO, msg=f"writing api activities to cache")
        with open(PATH_CACHE_API_ACTIVITIES, "w") as file:
            json.dump(data, file, indent=4)


    async def refresh(self) -> None:
        """
        """
        self.bot.logger.log(level=logging.INFO, msg=f"fetching api settings data from settings keys")
        settings = self.bot.api_client.fetch_api_settings(setting_ids=API_URL_SETTINGS_IDS)
        self.bot.logger.log(level=logging.INFO, msg=f"fetching api activities data from settings data")
        activities = self.bot.api_client.fetch_api_activities(settings=settings)
        self.bot.logger.log(level=logging.INFO, msg=f"comparing api activities data with last query")
        await self.compare_api_activities(self.bot.activities, activities)
        # await self.write_api_activities_cache(activities=activities)


    async def evaluate_new_api_activity(self, activity: APIClient.Activity) -> bool:
        """
        """
        has_id = hasattr(activity, "id")
        has_name = hasattr(activity, "name")
        has_image = hasattr(activity, "image")
        has_completions_limit = hasattr(activity, "completions_limit")
        has_reward_amount_to_reward = hasattr(activity, "reward_amount_to_reward")
        is_published = (has_id and has_name and has_image and has_completions_limit and has_reward_amount_to_reward)
        return is_published


    async def evaluate_old_api_activity(self, activity_old: dict, activity_new: APIClient.Activity) -> bool:
        """
        """
        is_different = False
        if (activity_new.data != activity_old):
            is_different = True
        return is_different


    async def compare_api_activities(self, activities_old: dict, activities_new: dict[str, APIClient.Activity]) -> None:
        """
        """
        cog_api_activities = self.bot.get_cog("APIActivities")
        keys_old = activities_old.keys()
        keys_new = activities_new.keys()
        is_different = False
        for key in keys_new:
            activity_new = activities_new[key]
            if key not in keys_old:
                if cog_api_activities:
                    self.bot.logger.log(level=logging.INFO, msg=f"detected new activity for key {key}, evaluating whether activity is live")
                    is_published = await self.evaluate_new_api_activity(activity=activity_new)
                    if is_published:
                        is_different = True
                        self.bot.logger.log(level=logging.INFO, msg=f"\tdetermined activity {activity_new.key} is live")
                        await self.send_api_activity_notification(activity=activity_new)
                    else:
                        self.bot.logger.log(level=logging.INFO, msg=f"\tdetermined activity {activity_new.key} is not live")
            else:
                self.bot.logger.log(level=logging.INFO, msg=f"detected old activity for key {key}, evaluating activity for api changes")
                activity_old = activities_old[key]
                if cog_api_activities:
                    is_changed = await self.evaluate_old_api_activity(activity_old=activity_old, activity_new=activity_new)
                    if is_changed:
                        is_different = True
                        self.bot.logger.log(level=logging.INFO, msg=f"\tchanges detected for activity {key}")
                        self.bot.logger.log(level=logging.INFO, msg=f"\tchanged \n\t{activity_old}\nto\n\t{activity_new.data}")
                        # TODO : send message to logging channel in different method
                    else:
                        self.bot.logger.log(level=logging.INFO, msg=f"\tchanges not detected for activity {key}")
        activities = activities_new
        for key in keys_old:
            if key not in keys_new:
                activities[key] = activities_old[key]
                # comment about idea -> if change is detected, write old data rather than [] to cache? or rely on logs for data changes from cache
        if is_different:
            self.bot.activities = activities_new
            await self.write_api_activities_cache(self.bot.activities)


    async def send_api_activity_notification(self, activity: APIClient.Activity, is_timed: bool = False) -> None:
        """
        """
        channel = self.bot.get_channel(DISCORD_CHANNEL_ID_TESTING)
        if channel:
            await channel.send(
                content=self.bot.api_client.generate_api_activity_content(), 
                embed=self.bot.api_client.generate_api_activity_embed(activity=activity)
            )


async def setup(bot: Club9Bot) -> None:
    """
    """
    await bot.add_cog(APIActivities(bot))
