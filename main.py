
from config.config import *
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os
from typing import Final
from utils.api_client import APIClient


class Club9Bot(commands.Bot):
    """
    """
    def __init__(self, command_prefix="!", intents=None, logger=logging.getLogger("discord")):
        """
        """
        intents = intents or discord.Intents.default()
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.logger = logger
        self.api_client = APIClient(self.logger)
        self.activities: dict = {}


    async def on_ready(self) -> None:
        """
        """
        self.logger.log(level=logging.INFO, msg="loading api activities cog")
        await self.load_extension("cogs.api_activities")
        
        cog_api_activities = self.get_cog("APIActivities")
        if cog_api_activities:
            self.logger.log(level=logging.INFO, msg="calling api activities cog 'refresh' method")
            await cog_api_activities.read_api_activities_cache()
            await cog_api_activities.refresh()


def main():
    """
    """
    load_dotenv()
    TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename=PATH_DISCORD_LOGS(), encoding="utf-8", mode="w")
    handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
    logger.addHandler(handler)

    intents: discord.Intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True

    bot = Club9Bot(command_prefix="!", intents=intents, logger=logger)
    bot.run(token=TOKEN)


if __name__ == "__main__":
    main()
