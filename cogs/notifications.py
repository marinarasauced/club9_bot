
import discord
from discord.ext import commands
import json
import logging

from config.config import *
from main import Club9Bot


class Club9Notifications(commands.Cog):
    """
    This class provides methods to send and edit notifications consisting of text content and a discord embed.

    @param bot: The Club9Bot to load this cog.
    """
    def __init__(self, bot: Club9Bot):
        """
        Initializes the Club9 activities cog.
        """
        self.club9_bot = bot


    async def read_cache(self) -> None:
        """
        Reads a cache file storing message ids for previous messages/notifications.
        """
        try:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Notifications -> reading messages cache")
            with open(PATH_MESSAGES_CACHE, "r") as file:
                self.club9_bot.messages_dict = json.load(file)
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Notifications -> read messages cache")
        except FileNotFoundError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Notifications -> failed to read messages cache (file not found)")
        except json.JSONDecodeError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Notifications -> failed to decode messages cache (json decode error)")
        except Exception as e:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Notifications -> failed to read messages cache ({e})")


    async def write_cache(self) -> None:
        """
        Writes a cache storing the current messages data for messages/notifications in Discord channels.
        """
        try:
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Notifications -> writing messages cache")
            with open(PATH_MESSAGES_CACHE, "w") as file:
                json.dump(self.club9_bot.messages_dict, file, indent=4)
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Notifications -> wrote messages cache")
            # self.club9_bot.num_activities_cache_write += 1
        except FileNotFoundError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Notifications -> failed to write messages cache (file not found)")
        except json.JSONDecodeError:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Notifications -> failed to decode messages cache (json decode error)")
        except Exception as e:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Notifications -> failed to write messages cache ({e})")


    async def send_notification(self, channel_id: int, content: str, embed: discord.Embed = None, type: str = None, id: int = None) -> discord.Message:
        """
        Sends a message to a channel consisting of a content string and a discord embed.
        
        @param channel_id: The id number of the channel in which the message is to be sent.
        @param content: The string content of the message (i.e., a role ping, some text).
        @param embed: The discord embed containing an image, the title, a description, and other text.
        @return The sent discord message object, or None if the channel wasn't found.
        """
        if (type is None or id is None):
            return None
        message_type = type.capitalize()
        if message_type not in ["Rewards", "Activities"]:
            return None
        channel = self.club9_bot.get_channel(channel_id)
        if channel:
            message = await channel.send(content=content, embed=embed)
            # self.club9_bot.num_activities_new_notifications += 1
            self.club9_bot.messages_dict[message_type].append({id: message.id})
            return message
        return None


    async def edit_notification(self, message: discord.Message):
        """
        """
        pass


async def setup(bot: Club9Bot) -> None:
    """
    Adds the cog to the discord bot during extension load.
    """
    await bot.add_cog(Club9Notifications(bot))
