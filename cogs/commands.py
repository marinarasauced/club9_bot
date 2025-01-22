
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
        self.monitoring_flag1 = False       # true when running, false otherwise
        self.monitoring_flag2 = False       # true if stopping, false otherwise
        self.runtime_start = time.time()


    async def validate(self, channel_id: int) -> bool:
        """
        Validates whether a command executed in the channel corresponding to the channel id attribute is permitted to run.
        
        @param channel_id: The id of the channel in which a command was executed.
        @return: True if the command is permitted to be executed, False otherwise.
        """
        if (channel_id == DISCORD_CHANNEL_ID_CLUB9_BOT_COMMANDS):
            return True         # permitted to execute
        return False        # not permitted to execute


    @commands.command(name="monitoring")
    async def monitoring(self, ctx, type: str = "", period: int = None) -> None:
        """
        Starts or stops monitoring of the Club9 activities and rewards on a timer.

        @param ctx:
        @param type: 'Start' or 'Stop' (not case sensitive)
        @param period: The period of the timer at which the monitoring method is called (period > 60)
        """
        # validate whether the command is permitted to execute
        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> user called '{self.club9_bot.command_prefix}monitoring {type} {period}'")
        if (await self.validate(channel_id=ctx.channel.id) == False):
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{self.club9_bot.command_prefix}monitoring {type} {period}' (not permitted to execute command in channel {ctx.channel.id})")
            return

        # determine whether command fields are valid
        monitoring_type = type.capitalize()
        if (monitoring_type not in ["Start", "Stop"]) or (period is None or period < 60):
            await ctx.send(f"""
the monitoring command must be formatted as follows:
`{self.club9_bot.command_prefix}monitoring type period`,
where `type` must be "start" or "stop" and `period` must be an integer greater than 60;
i.e., `{self.club9_bot.command_prefix}monitoring start 60`
            """)
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{self.club9_bot.command_prefix}monitoring {type} {period}' (invalid attribute 'type' or 'period')")
            return

        # if command is to start monitoring
        if (monitoring_type == "Start"):

            # if monitoring_flag2 is true, monitoring is already stopping
            if (self.monitoring_flag2 == True):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{self.club9_bot.command_prefix}monitoring {type} {period}' (monitoring is stopping)")
                await ctx.send("monitoring is already started!")
                return

            # if monitoring_flag1 is true, monitoring was already started
            if (self.monitoring_flag1 == True):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{self.club9_bot.command_prefix}monitoring {type} {period}' (monitoring was already started)")
                await ctx.send("monitoring is already started!")
                return
            
            # start monitoring
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> accepted user command '{self.club9_bot.command_prefix}monitoring {type} {period}'")
            await ctx.send(f"starting monitoring with a period of {period} seconds")
            try:
                self.monitoring_flag1 = True
                await self.club9_bot.wait_until_ready()
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> started monitoring activities and rewards with period {period}")
                while (self.monitoring_flag1 == True):
                    if (self.club9_bot.club9_cog_activities):
                        await self.club9_bot.club9_cog_activities.refresh()
                    if (self.club9_bot.club9_cog_rewards):
                        await self.club9_bot.club9_cog_rewards.refresh()
                    await asyncio.sleep(period)
            except Exception as e:
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> monitoring activities and rewards failed")
                await ctx.send(f"monitoring failed")
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> stopped monitoring activities and rewards with period {period}")
            await ctx.send(f"stopped monitoring with a period of {period} seconds")
            self.monitoring_flag2 = False

        # if command is to stop monitoring
        if (monitoring_type == "Stop"):

            # if monitoring_flag1 is false, monitoring was already stopped
            if (self.monitoring_flag1 == False):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{self.club9_bot.command_prefix}monitoring {type}' (monitoring is already stopped)")
                await ctx.send("monitoring is already stopped!")
                return

            # if monitoring_flag2 is true, monitoring is already stopping
            if (self.monitoring_flag2 == True):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{self.club9_bot.command_prefix}monitoring {type}' (monitoring is already stopping)")
                await ctx.send("monitoring is already stopping!")
                return

            # stop monitoring
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> accepted user command '{self.club9_bot.command_prefix}monitoring {type}'")
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> stopping monitoring activities and rewards")
            await ctx.send(f"stopping monitoring at the end of the current period")
            self.monitoring_flag1 = False
            self.monitoring_flag2 = True


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
