
import asyncio
from discord.ext import commands
import logging
import time

from config.config import *
from main import Club9Bot


class Club9Commands(commands.Cog):
    """
    This class includes Club9Bot commands available in discord.

    @param bot: The Club9Bot to load this cog.
    """
    def __init__(self, bot: Club9Bot):
        """
        Initializes the Club9 activities cog.
        """
        self.club9_bot = bot
        self.monitoring_flag = False
        self.runtime_start = time.time()


    @commands.command(name="monitoring_start")
    async def monitoring_start(self, ctx, period: int = 300) -> None:
        """
        Starts the Club9Bot's monitoring cycle.

        This command method starts the monitoring cycle during which the bot will call its refresh methods on a timer.

        @param ctx: The context of the command.
        @param period: The period at which the monitoring cycle is conducted (i.e., period = 300 (seconds) means that the refresh methods are called once every five minutes)
        """
        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> user called '{self.club9_bot.command_prefix}monitoring_start {period}'")
        if (ctx.channel.id != DISCORD_CHANNEL_ID_CLUB9_BOT_COMMANDS):
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{self.club9_bot.command_prefix}monitoring_start {period}' (not executed in permitted channel)")
            return
        if self.monitoring_flag:
            await ctx.send("Monitoring is already running!")
            return
        if period < 30:
            await ctx.send("The period must be at least 30 seconds.")
            self.club9_bot.logger.log(level=logging.ERROR, msg="Club9Commands -> period must be greater than or equal to 30 seconds")
            return
        self.monitoring_flag = True
        await ctx.send(f"starting monitoring with a period of {period} seconds.")
        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> starting monitoring with period {period}")
        await self.club9_bot.wait_until_ready()
        while self.monitoring_flag:
            if self.club9_bot.club9_cog_activities:
                await self.club9_bot.club9_cog_activities.refresh()
                await asyncio.sleep(period)
        await ctx.send("stopped monitoring.")
        self.club9_bot.logger.log(level=logging.INFO, msg="Club9Commands -> monitoring stopped.")


    @commands.command(name="monitoring_stop")
    async def monitoring_stop(self, ctx) -> None:
        """
        Stops the Club9Bot's monitoring cycle.

        This command stops the monitoring cycle by setting the flag to False.
        @param ctx: The context of the command.
        """
        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> user called '{self.club9_bot.command_prefix}monitoring_stop'")
        if (ctx.channel.id != DISCORD_CHANNEL_ID_CLUB9_BOT_COMMANDS):
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{self.club9_bot.command_prefix}monitoring_stop' (not executed in permitted channel)")
            return
        if not self.monitoring_flag:
            await ctx.send("Monitoring is not currently running!")
            return
        self.monitoring_flag = False
        await ctx.send("stopping monitoring at the end of the current period.")
        self.club9_bot.logger.log(level=logging.INFO, msg="Club9Commands -> stopping monitoring at the end of the current period.")


    @commands.command(name="runtime")
    async def runtime(self, ctx) -> None:
        """
        Prints the bot's runtime and stats like number of new quests, number of message edits, etc.

        @param ctx: The context of the command.
        """
        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> user called '{self.club9_bot.command_prefix}runtime'")
        if (ctx.channel.id != DISCORD_CHANNEL_ID_CLUB9_BOT_COMMANDS):
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{self.club9_bot.command_prefix}runtime' (not executed in permitted channel)")
            return
        runtime_curr = time.time() - self.runtime_start
        days = int(runtime_curr // 86400)  # 1 day = 86400 seconds
        hours = int((runtime_curr % 86400) // 3600)  # 1 hour = 3600 seconds
        minutes = int((runtime_curr % 3600) // 60)  # 1 minute = 60 seconds
        seconds = round(runtime_curr % 60) 
        runtime_formatted = f"{days} day{'' if days == 1 else 's'} {hours:02}:{minutes:02}:{seconds:02}"
        await ctx.send(f"""
Runtime: {runtime_formatted}
Num of activity cache reads: {self.club9_bot.num_activities_cache_read}
Num of activity cache writes: {self.club9_bot.num_activities_cache_write}
Num of new activities detected: {self.club9_bot.num_activities_new_detected}
Num of new activity notifications: {self.club9_bot.num_activities_new_notifications}
""")
        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> returned runtime as {runtime_formatted}")


async def setup(bot: Club9Bot) -> None:
    """
    Adds the cog to the discord bot during extension load.
    """
    await bot.add_cog(Club9Commands(bot))
