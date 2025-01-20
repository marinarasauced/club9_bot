
import discord
from discord.ext import commands
from http.cookiejar import MozillaCookieJar
import logging
import requests
import re

from config.config import *
from main import Club9Bot
from utils.reward import Club9RewardType


class Club9Rewards(commands.Cog):
    """
    This class provides methods to send and edit reward diagnostics via a discord embed.

    @param bot: The Club9Bot to load this cog.
    """
    def __init__(self, bot: Club9Bot):
        """
        Initializes the Club9 activities cog.
        """
        self.club9_bot = bot
        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> loading Club9 site cookies")
        try:
            cookies = MozillaCookieJar()
            cookies.load(PATH_COOKIES, ignore_discard=True, ignore_expires=True)
            self.cookies = {cookie.name: cookie.value for cookie in cookies}
            self.session = requests.Session()
            self.session.cookies.update(self.cookies)
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> loaded Club9 site cookies")
        except:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> failed to load Club9 site cookies")


    async def parse(self, category: Club9RewardType = Club9RewardType.NONE) -> dict[str, str]:
        """
        Parses the Club9 Rewards page HTML to determine rewards in a given category and fetches corresponding rewards data from API.

        @param category: The Club9 reward type 'category'.
        @return: A dictionary of reward handle names to the respective fetched data.
        """
        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> parsing shop for {category} rewards")
        cat_url = None
        cat_string = None
        if (category == Club9RewardType.NONE):
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> invalid reward category")
            return {}
        elif (category == Club9RewardType.ELITE):
            cat_url = REWARDS_ELITE_URL
            cat_string = REWARDS_ELITE_SEARCH_STRING
        elif (category == Club9RewardType.MASTER):
            cat_url = REWARDS_MASTER_URL
            cat_string = REWARDS_MASTER_SEARCH_STRING
        elif (category == Club9RewardType.CHAMPION):
            cat_url = REWARDS_CHAMPION_URL
            cat_string = REWARDS_CHAMPION_SEARCH_STRING
        elif (category == Club9RewardType.LEGENDARY):
            cat_url = REWARDS_LEGENDARY_URL
            cat_string = REWARDS_LEGENDARY_SEARCH_STRING
        elif (category == Club9RewardType.MASTER):
            cat_url = REWARDS_MASTER_URL
            cat_string = REWARDS_MYTHIC_URL
        try:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> fetching html data for {category} rewards")
            response = self.session.get(url=cat_url)
            html = response.text
            pattern = rf"[\"']({re.escape(cat_string)}.*?)[\"']"        
            matches = re.findall(pattern, html)
            rewards_names = sorted(set(matches))
            if not rewards_names:
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> no rewards data found for {category} category")
                return {}
            for i in range(len(rewards_names)):
                rewards_names[i] = rewards_names[i].split("/")[-1]
            rewards_query = ' OR '.join([f'handle:"{reward}"' for reward in rewards_names])
            data_url = REWARDS_QUERY_URL + rewards_query
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> fetching rewards data for {category} rewards")
            response = self.session.get(url=data_url)
            rewards_data = response.json()
            rewards_items = rewards_data.get("Items")
            rewards_dict = {}
            for reward_item in rewards_items:
                reward_key = reward_item.get("handle", None)
                if reward_key is not None and reward_key in rewards_names:
                    rewards_dict[reward_key] = reward_item
            return rewards_dict
        except Exception as e:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> failed to parse rewards {e}")
            return {}





    # async def send_notification(self, channel_id: int, content: str, embed: discord.Embed = None) -> discord.Message:
    #     """
    #     Sends a message to a channel consisting of a content string and a discord embed.
        
    #     @param channel_id: The id number of the channel in which the message is to be sent.
    #     @param content: The string content of the message (i.e., a role ping, some text).
    #     @param embed: The discord embed containing an image, the title, a description, and other text.
    #     @return The sent discord message object, or None if the channel wasn't found.
    #     """
    #     channel = self.club9_bot.get_channel(channel_id)
    #     if channel:
    #         message = await channel.send(content=content, embed=embed)
    #         self.club9_bot.num_activities_new_notifications += 1
    #         return message
    #     return None


    # async def edit_notification(self, message: discord.Message):
    #     """
    #     """
    #     pass


async def setup(bot: Club9Bot) -> None:
    """
    Adds the cog to the discord bot during extension load.
    """
    await bot.add_cog(Club9Rewards(bot))

