
import discord
from discord.ext import commands
import logging

from config.config import *
from main import Club9Bot


class Club9Logging(commands.Cog):
    """
    This class provides methods to log bot operations to the bot-logs channel using discord embeds.
    """
    def __init__(self, bot: Club9Bot):
        """
        Initializes the Club9Bot logging cog.
        """
        self.club9_bot = bot


    async def log_send_notification(self, message: discord.Message, content: str = "sent notification ->") -> None:
        """
        """
        channel = self.club9_bot.get_channel(DISCORD_CHANNEL_ID_CLUB9_BOT_LOGS)
        if (channel and message.embeds):
            for embed in message.embeds:
                await channel.send(
                    content=content,
                    embed=embed
                )


    async def log_edit_notification(self, message: discord.Message, content: str) -> None:
        """
        """
        channel = self.club9_bot.get_channel(DISCORD_CHANNEL_ID_CLUB9_BOT_LOGS)
        if (channel and message.embeds):
            for embed in message.embeds:
                await channel.send(
                    content=content,
                    embed=embed
                )

    async def log_delete_notification(self, message: discord.Message, content: str = "deleted notification ->") -> None:
        """
        """
        channel = self.club9_bot.get_channel(DISCORD_CHANNEL_ID_CLUB9_BOT_LOGS)
        if (channel and message.embeds):
            for embed in message.embeds:
                await channel.send(
                    content=content,
                    embed=embed
                )


async def setup(bot: Club9Bot) -> None:
    """
    Adds the cog to the discord bot during extension load.
    """
    await bot.add_cog(Club9Logging(bot))
