
import asyncio
from discord.ext import commands
import logging

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


    @commands.command(name="monitoring_start")
    async def monitoring_start(self, ctx, period: int = 300) -> None:
        """
        Starts the Club9Bot's monitoring cycle.

        This command method starts the monitoring cycle during which the bot will call its refresh methods on a timer.

        @param ctx: The context of the command.
        @param period: The period at which the monitoring cycle is conducted (i.e., period = 300 (seconds) means that the refresh methods are called once every five minutes)
        """
        if self.monitoring_flag:
            await ctx.send("Monitoring is already running!")
            return

        if period < 30:
            await ctx.send("The period must be at least 30 seconds.")
            self.club9_bot.logger.log(level=logging.ERROR, msg="Club9Commands -> period must be greater than or equal to 30 seconds")
            return

        self.monitoring_flag = True
        await ctx.send(f"Starting monitoring with a period of {period} seconds.")
        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> Starting monitoring with period {period}")

        await self.club9_bot.wait_until_ready()
        while self.monitoring_flag:
            if self.club9_bot.club9_cog_activities:
                await self.club9_bot.club9_cog_activities.refresh()
                await asyncio.sleep(period)

        await ctx.send("Monitoring stopped.")
        self.club9_bot.logger.log(level=logging.INFO, msg="Club9Commands -> Monitoring stopped.")


    @commands.command(name="monitoring_stop")
    async def monitoring_stop(self, ctx) -> None:
        """
        Stops the Club9Bot's monitoring cycle.

        This command stops the monitoring cycle by setting the flag to False.
        @param ctx: The context of the command.
        """
        if not self.monitoring_flag:
            await ctx.send("Monitoring is not currently running!")
            return

        self.monitoring_flag = False
        await ctx.send("Stopping monitoring. It will stop at the end of the current period.")
        self.club9_bot.logger.log(level=logging.INFO, msg="Club9Commands -> Stopping monitoring.")


    @commands.command(name="runtime")
    async def runtime(self, ctx) -> None:
        """
        Prints the bot's runtime and stats like number of new quests, number of message edits, etc.

        @param ctx: The context of the command.
        """


async def setup(bot: Club9Bot) -> None:
    """
    Adds the cog to the discord bot during extension load.
    """
    await bot.add_cog(Club9Commands(bot))
