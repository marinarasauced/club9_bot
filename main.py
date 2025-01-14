
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os
import time
from typing import Final

from config.config import *
from utils.api import Club9API


class Club9Bot(commands.Bot):
    """
    """
    def __init__(self, command_prefix="!", intents=None, logger=logging.getLogger("discord")):
        """
        """
        intents = intents or discord.Intents.default()
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.logger = logger
        self.api = Club9API(self.logger)

        self.activities_dict: dict = {}
        self.activities_mapping: dict = {}  # map of activity ids to Club9Activity objects generated on startup for comparison to requests during refresh comparison
        # TODO add mapping attribute dict for tracking messages in case of editing quests upon api change
        self.runtime_start = time.time()


    async def on_ready(self) -> None:
        """
        """
        await self.load_extension("cogs.commands")
        self.club9_cog_commands = self.get_cog("Club9Commands")

        await self.load_extension("cogs.notifications")
        self.club9_cog_notifications = self.get_cog("Club9Notifications")
        # if self.club9_cog_notifications:    async def 
            # await self.club9_cog_notifications.send_notification(channel_id=DISCORD_CHANNEL_ID_CLUB9_NOTIFICATIONS, content="test2")

        await self.load_extension("cogs.activities")
        self.club9_cog_activities = self.get_cog("Club9Activities")
        if self.club9_cog_activities:
            await self.club9_cog_activities.read_cache()
            await self.club9_cog_activities.refresh()


        # self.logger.log(level=logging.INFO, msg="loading api activities cog")
        # await self.load_extension("cogs.api_activities")
        
        # cog_api_activities = self.get_cog("APIActivities")
        # if cog_api_activities:
        #     self.logger.log(level=logging.INFO, msg="calling api activities cog 'refresh' method")
        #     await cog_api_activities.read_api_activities_cache()
        #     await cog_api_activities.refresh()

        #     self.loop.create_task(self.query())
    



    # async def query(self) -> None:
    #     """
    #     """
    #     await self.wait_until_ready()
    #     while not self.is_closed():
    #         cog_api_activities = self.get_cog("APIActivities")
    #         if cog_api_activities:
    #             self.logger.log(level=logging.INFO, msg="calling api activities cog 'refresh' method")
    #             await cog_api_activities.refresh()
    #             await asyncio.sleep(300)


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
