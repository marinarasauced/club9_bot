
import discord
from discord.ext import commands
from http.cookiejar import MozillaCookieJar
import logging
import requests
import re

from config.config import *
from main import Club9Bot
from utils.reward import (
    Club9RewardType,
    get_reward_types,
    get_reward_channel_id,
    generate_reward_embed,
)
import json

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


    async def read_cache(self) -> None:
        """
        Reads a cache file storing the previous rewards data for each tier.

        This method reads a JSON cache file and assigns the data to a bot attribute in order to speed up fetching.
        """
        try:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> reading rewards cache")
            with open(PATH_REWARDS_CACHE, "r") as file:
                self.club9_bot.rewards_dict = json.load(file)
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> read rewards cache")
        except FileNotFoundError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Rewards -> failed to read rewards cache (file not found)")
        except json.JSONDecodeError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Rewards -> failed to decode rewards cache (json decode error)")
        except Exception as e:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Rewards -> failed to read rewards cache ({e})")


    async def write_cache(self) -> None:
        """
        Writes a cache file storing the current rewards data for each tier.

        This method writes a JSON cache file and assigns the data from the bot's rewards data attribute to the file. Upon startup, this cache is read, giving the bot a baseline to compare refreshes with.
        """
        try:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> writing rewards cache")
            with open(PATH_REWARDS_CACHE, "w") as file:
                json.dump(self.club9_bot.rewards_dict, file, indent=4)
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> wrote rewards cache")
            # self.club9_bot.num_activities_cache_write += 1
        except FileNotFoundError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Rewards -> failed to write rewards cache (file not found)")
        except json.JSONDecodeError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Rewards -> failed to decode rewards cache (json decode error)")
        except Exception as e:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Rewards -> failed to write rewards cache ({e})")


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
        elif (category == Club9RewardType.MYTHIC):
            cat_url = REWARDS_MYTHIC_URL
            cat_string = REWARDS_MYTHIC_SEARCH_STRING
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
                reward_handle = reward_item.get("handle", None)
                reward_id = reward_item.get("id", None)
                if (reward_id is not None and reward_handle is not None and reward_handle in rewards_names):
                    rewards_dict[reward_id] = reward_item
            return rewards_dict
        except Exception as e:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> failed to parse rewards ({e})")
            return {}


    async def refresh(self) -> None:
        """
        """
        try:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> refreshing rewards")
            rewards_dict: dict = {}
            is_cache_rewards_outdated: bool = False
            is_cache_messages_outdated: bool = False
            for reward_type in Club9RewardType.__members__.values():
                if (reward_type is not Club9RewardType.NONE):
                    rewards_dict[reward_type.value] = await self.club9_bot.club9_cog_rewards.parse(category=reward_type)
            if (rewards_dict == self.club9_bot.rewards_dict):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> refreshed rewards (no changes detected)")
            else:
                for category in get_reward_types():
                    rewards_data_old = self.club9_bot.rewards_dict[category]
                    rewards_data_new = rewards_dict[category]
                    if (rewards_data_new == rewards_data_old):
                        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> detected no changes to {category} rewards")
                    else:
                        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> detected changes to {category} rewards")
                        rewards_ids_old = rewards_data_old.keys()
                        rewards_ids_new = rewards_data_new.keys()
                        # detect if any rewards were added
                        for reward_id in rewards_ids_new:
                            if (reward_id not in rewards_ids_old):
                                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> detected reward {reward_id} added to {category}")
                                reward_data_new = rewards_data_new[reward_id]
                                embed = generate_reward_embed(reward_data=reward_data_new, category=category)
                                channel_id = get_reward_channel_id(category)
                                await self.club9_bot.club9_cog_notifications.send_notification(channel_id=channel_id, content="", embed=embed, type="Rewards", id=reward_id)
                                is_cache_rewards_outdated = True
                                is_cache_messages_outdated = True
                        # detect if any rewards were removed
                        for reward_id in rewards_ids_old:
                            if (reward_id not in rewards_ids_new):
                                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> detected reward {reward_id} removed from {category}")
                                await self.club9_bot.club9_cog_notifications.delete_notification(type="Rewards", id=reward_id)
                                is_cache_rewards_outdated = True
                                is_cache_messages_outdated = True
                            else:
                                # check if reward was modified
                                reward_data_old = rewards_data_old.get(reward_id)
                                reward_data_new = rewards_data_new.get(reward_id)
                                if (reward_data_old == reward_data_new):
                                    # no change to specific reward
                                    self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> detected no changes to reward {reward_id} in {category}")
                                else:
                                    # change detected
                                    self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Rewards -> detected changes to reward {reward_id} in {category}")
                                    embed = generate_reward_embed(reward_data=reward_data_new, category=category)
                                    channel_id = get_reward_channel_id(category)
                                    await self.club9_bot.club9_cog_notifications.edit_notification(content=None, embed=embed, type="Rewards", id=reward_id)
                                    is_cache_rewards_outdated = True
                                    # messages cache not outdated since no change to message/channel ids
            if (is_cache_rewards_outdated == True):
                self.club9_bot.rewards_dict = rewards_dict
                await self.club9_bot.club9_cog_rewards.write_cache()
            if (is_cache_messages_outdated == True):
                await self.club9_bot.club9_cog_notifications.write_cache()
        except Exception as e:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Rewards -> failed to refresh rewards ({e})")


async def setup(bot: Club9Bot) -> None:
    """
    Adds the cog to the discord bot during extension load.
    """
    await bot.add_cog(Club9Rewards(bot))

