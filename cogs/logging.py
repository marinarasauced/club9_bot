
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


    async def log_notification_event(self, message: discord.Message, content: str) -> None:
        """
        Logs a Club9Bot discord message event including notification sends, edits, and deletes.

        @param message: the discord message that the event is pertaining to.
        @param content: the nature of the event.
        """
        try:
            channel = self.club9_bot.get_channel(DISCORD_CHANNEL_ID_CLUB9_BOT_LOGS)
            if (channel and message.embeds):
                for message_embed in message.embeds:
                    embed = discord.Embed.copy(message_embed)
                    await channel.send(
                        content=content,
                        embed=embed
                    )
        except Exception as e:
            self.club9_bot.logger.log(level=logging.ERROR, msg=f"Club9Logging -> failed to log notification event ({e})")


async def setup(bot: Club9Bot) -> None:
    """
    Adds the cog to the discord bot during extension load.
    """
    await bot.add_cog(Club9Logging(bot))
