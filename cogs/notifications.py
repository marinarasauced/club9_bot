
import discord
from discord.ext import commands
import logging

from config.config import *
from main import Club9Bot


class Club9Notifications(commands.Cog):
    """
    This class provides a methods to send and edit notifications consisting of text content and a discord embed.

    @param bot: The Club9Bot to load this cog.
    """
    def __init__(self, bot: Club9Bot):
        """
        Initializes the Club9 activities cog.
        """
        self.club9_bot = bot


    async def send_notification(self, channel_id: int, content: str, embed: discord.Embed = None) -> discord.Message:
        """
        Sends a message to a channel consisting of a content string and a discord embed.
        
        @param channel_id: The id number of the channel in which the message is to be sent.
        @param content: The string content of the message (i.e., a role ping, some text).
        @param embed: The discord embed containing an image, the title, a description, and other text.
        @return The sent discord message object, or None if the channel wasn't found.
        """
        channel = self.club9_bot.get_channel(channel_id)
        if channel:
            message = await channel.send(content=content, embed=embed)
            print(message)
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
