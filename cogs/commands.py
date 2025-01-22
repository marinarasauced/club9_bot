
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

        @param ctx: The context of the command.
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
        if (
            (monitoring_type not in ["Start", "Stop"]) or 
            (monitoring_type == "Start" and (period is None or period < 60))
        ):
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
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> started monitoring activities and rewards with period {period} seconds")
                while (self.monitoring_flag1 == True):
                    if (self.club9_bot.club9_cog_activities):
                        await self.club9_bot.club9_cog_activities.refresh()
                    if (self.club9_bot.club9_cog_rewards):
                        await self.club9_bot.club9_cog_rewards.refresh()
                    self.club9_bot.num_monitoring_cycles += 1
                    await asyncio.sleep(period)
            except Exception as e:
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> monitoring activities and rewards failed")
                await ctx.send(f"monitoring failed")
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> stopped monitoring activities and rewards with period {period} seconds")
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


    @commands.command(name="status")
    async def status(self, ctx) -> None:
        """
        Returns the bot's status including runtime and num attributes counting tasks performed.

        @param ctx: The context of the command.
        """
        # validate whether the command is permitted to execute
        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> user called '{self.club9_bot.command_prefix}status'")
        if (await self.validate(channel_id=ctx.channel.id) == False):
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{self.club9_bot.command_prefix}status' (not permitted to execute command in channel {ctx.channel.id})")
            return
        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> accepted user command '{self.club9_bot.command_prefix}status'")
    
        # format runtime
        runtime = time.time() - self.club9_bot.starttime
        days = int(runtime // 86400)
        hours = int((runtime % 86400) // 3600)
        minutes = int((runtime % 3600) // 60)
        seconds = round(runtime % 60)

        # format response
        response = f"""```py
# general diagnostics
runtime = "{days} day{'' if days == 1 else 's'} {hours:02}:{minutes:02}:{seconds:02}"
num_monitoring_cycles = {self.club9_bot.num_monitoring_cycles}

# activities diagnostics
num_activities_cache_reads = {self.club9_bot.num_activities_cache_reads}
num_activities_cache_writes = {self.club9_bot.num_activities_cache_writes}
num_detected_activities_added = {self.club9_bot.num_activities_added}
num_detected_activities_removed = {self.club9_bot.num_activities_removed}
num_detected_activities_modified = {self.club9_bot.num_activities_modified}

# rewards diagnostics
num_rewards_cache_reads = {self.club9_bot.num_rewards_cache_reads}
num_rewards_cache_writes = {self.club9_bot.num_rewards_cache_writes}
num_detected_rewards_added = {self.club9_bot.num_rewards_added}
num_detected_rewards_removed = {self.club9_bot.num_rewards_removed}
num_detected_rewards_modified = {self.club9_bot.num_rewards_modified}
```"""
        
        # send response
        await ctx.send(response)


async def setup(bot: Club9Bot) -> None:
    """
    Adds the cog to the discord bot during extension load.
    """
    await bot.add_cog(Club9Commands(bot))
