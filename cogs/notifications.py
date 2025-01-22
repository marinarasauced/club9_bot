
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
        Initializes the Club9 notifications cog.
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


    async def send_notification(self, channel_id: int, content: str, embed: discord.Embed, type: str, id: int) -> discord.Message:
        """
        Sends a message to a channel consisting of a content string and a discord embed.
        
        @param channel_id: The id number of the channel in which the message is to be sent.
        @param content: The string content of the message (i.e., a role ping, some text).
        @param embed: The discord embed containing an image, the title, a description, and other text.
        @param type: 
        @param id:
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
            await self.club9_bot.club9_cog_logging.log_send_notification(message=message)
            self.club9_bot.messages_dict[message_type][id] = {
                "channel_id": channel_id,
                "message_id": message.id
            }
            return message
        return None


    async def edit_notification(self, content: str, embed: discord.Embed, type: str, id: int) -> None:
        """
        Edits a message in a channel consisting of a content string and a discord embed.

        @param content: The new string content.
        @param embed: The new embed object.
        @param type: 
        @param id:
        """
        if (type is None or id is None):
            return
        message_type = type.capitalize()
        if message_type not in ["Rewards", "Activities"]:
            return
        data = self.club9_bot.messages_dict[type][id]
        channel_id = data.get("channel_id", None)
        message_id = data.get("message_id", None)
        channel = self.club9_bot.get_channel(channel_id)
        if channel:
            try:
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Notifications -> editing message {message_id} in channel {channel_id}")
                message = await channel.fetch_message(message_id)
                await self.club9_bot.club9_cog_logging.log_edit_notification(message=message, content="edited notification from ->")
                if (content is not None and embed is not None):
                    await message.edit(content=content, embed=embed)
                elif (content is None and embed is not None):
                    await message.edit(embed=embed)
                elif (content is not None and embed is None):
                    await message.edit(content=content)
                await self.club9_bot.club9_cog_logging.log_edit_notification(message=message, content="to ->")
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Notifications -> edited message {message_id} in channel {channel_id}")
            except Exception as e:
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Notifications -> unable to edit message {message_id} in channel {channel_id} ({e})")


    async def delete_notification(self, type: str, id: int) -> None:
        """
        """
        if (type is None or id is None):
            return
        message_type = type.capitalize()
        if message_type not in ["Rewards", "Activities"]:
            return
        data = self.club9_bot.messages_dict[type][id]
        channel_id = data.get("channel_id", None)
        message_id = data.get("message_id", None)
        channel = self.club9_bot.get_channel(channel_id)
        if channel:
            try:
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Notifications -> deleting message {message_id} in channel {channel_id}")
                message = await channel.fetch_message(message_id)
                await self.club9_bot.club9_cog_logging.log_delete_notification(message=message)
                await message.delete()
                del self.club9_bot.messages_dict[message_type][id]
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Notifications -> deleted message {message_id} in channel {channel_id}")
            except Exception as e:
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Notifications -> unable to delete message {message_id} in channel {channel_id} ({e})")


async def setup(bot: Club9Bot) -> None:
    """
    Adds the cog to the discord bot during extension load.
    """
    await bot.add_cog(Club9Notifications(bot))
