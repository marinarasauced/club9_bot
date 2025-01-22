
import asyncio
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
        self.rewards_dict: dict = {}
        self.messages_dict: dict = {}

        # general diagnostics
        self.starttime = time.time()
        self.num_monitoring_cycles = 0

        # activities diagnostics
        self.num_activities_cache_reads = 0
        self.num_activities_cache_writes = 0
        self.num_activities_added = 0
        self.num_activities_removed = 0
        self.num_activities_modified = 0

        # rewards diagnostics
        self.num_rewards_cache_reads = 0
        self.num_rewards_cache_writes = 0
        self.num_rewards_added = 0
        self.num_rewards_removed = 0
        self.num_rewards_modified = 0


    async def on_ready(self) -> None:
        """
        """
        # load commands cog
        await self.load_extension("cogs.commands")
        self.club9_cog_commands = self.get_cog("Club9Commands")

        # load notifications cog
        await self.load_extension("cogs.notifications")
        self.club9_cog_notifications = self.get_cog("Club9Notifications")
        if self.club9_cog_notifications:
            await self.club9_cog_notifications.read_cache()

        # load activities cog
        await self.load_extension("cogs.activities")
        self.club9_cog_activities = self.get_cog("Club9Activities")
        if self.club9_cog_activities:
            await self.club9_cog_activities.read_cache()

        # load rewards cog
        await self.load_extension("cogs.rewards")
        self.club9_cog_rewards = self.get_cog("Club9Rewards")
        if self.club9_cog_rewards:
            await self.club9_cog_rewards.read_cache()

        # log bot is online
        self.logger.log(level=logging.INFO, msg="Club9Bot is online.")

        # if enabled, start monitoring activities and rewards
        if (ENABLE_MONITORING_ON_STARTUP_BOOL == True):
            channel = self.get_channel(DISCORD_CHANNEL_ID_CLUB9_BOT_COMMANDS)
            if (channel):
                message = await channel.send("executing '!monitoring start {ENABLE_MONITORING_ON_STARTUP_PERIOD} from backend")
                context = await self.get_context(message)
                command = self.get_command("monitoring")
                if command:
                    await context.invoke(command, type="Start", period=ENABLE_MONITORING_ON_STARTUP_PERIOD)


def main():
    """
    """
    # load env variables
    load_dotenv(dotenv_path=PATH_DOTENV)
    TOKEN: Final[str] = os.getenv(DISCORD_TOKEN_NAME)

    # setup logger
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename=PATH_DISCORD_LOGS(), encoding="utf-8", mode="w")
    handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
    logger.addHandler(handler)

    # setup intents
    intents: discord.Intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True

    # handle startup and shutdown
    bot = Club9Bot(command_prefix=DISCORD_COMMAND_PREFIX, intents=intents, logger=logger)
    bot.run(token=TOKEN)
    bot.logger.log(level=logging.INFO, msg="Club9Bot is offline.")
    asyncio.run(bot.close())


if __name__ == "__main__":
    main()
