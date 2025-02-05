
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
    async def monitoring(self, ctx, keyword1: str, keyword2: str = None) -> None:
        """
        Handles tasks pertaining to the bot's monitoring of the activities and rewards APIs.

        This method utilizes keyword arguments to execute specific sub tasks pertaining to monitoring:
            - 'monitoring start' starts the bot's monitoring using the default period from the config file for all enabled rewards types,
            - 'monitoring start period' starts the bot's monitoring using the given period value for all enabled types such as activities and rewards,
            - 'monitoring stop' stops the bot's monitoring at the end of the current monitoring cycle,
            - 'monitoring enable type' enables the bot's monitoring of a specfic type; i.e., activities or rewards,
            - 'monitoring disable type' disables the bot's monitoring of a specific type; i.e., activities or rewards,

        """
        keywords = MONITORING_KEYWORDS_1
        command = f'{self.club9_bot.command_prefix}monitoring {keyword1.lower()}'
        if (keyword2 != None and keyword2 != ""):
            command += f' {keyword2}'

        # validate whether the command is permitted to execute
        self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> user called '{command}'")
        if (await self.validate(channel_id=ctx.channel.id) == False):
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{command}' (not permitted to execute command in channel {ctx.channel.id})")
            return

        # validate whether command keyword1 is valid
        if (keyword1.lower() not in keywords):
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{command}' (keyword1 argument invalid)")
            return

        # case : start monitoring
        if (keyword1.lower() == "start"):

            # if monitoring_flag2 is true, monitoring is stopping
            if (self.monitoring_flag2 == True):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{command}' (monitoring is stopping)")
                await ctx.send("rejected command : monitoring is currently stopping")
                return

            # if monitoring_flag1 is true, monitoring was already started
            if (self.monitoring_flag1 == True):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{command}' (monitoring was already started)")
                await ctx.send("rejected command : monitoring was already started!")
                return

            # if period is command argument and period is not int or period is less than 60 seconds, period is invalid
            if (keyword2 != None and isinstance(keyword2, str) and int(keyword2) < 60):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{command}' (keyword2 argument invalid)")
                await ctx.send("rejected command : invalid command arguments")
                return

            # accept command
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> accepted user command '{command}'")
            period = ENABLE_MONITORING_ON_STARTUP_PERIOD
            if (keyword2 != None and isinstance(keyword2, str) and int(keyword2) >= 60):
                period = int(keyword2)
            await ctx.send(f"starting monitoring with a period of {period} seconds")
            try:
                self.monitoring_flag1 = True
                await self.club9_bot.wait_until_ready()
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> started monitoring activities and rewards with period {period} seconds")
                while (self.monitoring_flag1 == True):
                    if (self.club9_bot.club9_cog_activities and self.club9_bot.monitor_activities == True):
                        await self.club9_bot.club9_cog_activities.refresh()
                        self.club9_bot.num_activities_monitoring_cycles += 1
                    if (self.club9_bot.club9_cog_rewards and self.club9_bot.monitor_rewards == True):
                        await self.club9_bot.club9_cog_rewards.refresh()
                        self.club9_bot.num_rewards_monitoring_cycles += 1
                    await asyncio.sleep(period)
            except Exception as e:
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> monitoring activities and rewards failed")
                await ctx.send(f"monitoring failed")
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> stopped monitoring activities and rewards with period {period} seconds")
            await ctx.send(f"stopped monitoring with a period of {period} seconds")
            self.monitoring_flag2 = False

        # case : stop monitoring
        if (keyword1.lower() == "stop"):

            # if monitoring_flag1 is false, monitoring was already stopped
            if (self.monitoring_flag1 == False):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{self.club9_bot.command_prefix}monitoring {type}' (monitoring is already stopped)")
                await ctx.send("rejected command : monitoring was already stopped")
                return

            # if monitoring_flag2 is true, monitoring is already stopping
            if (self.monitoring_flag2 == True):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{self.club9_bot.command_prefix}monitoring {type}' (monitoring is already stopping)")
                await ctx.send("rejected command : monitoring is currently stopping")
                return

            # accept command
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> accepted user command '{self.club9_bot.command_prefix}monitoring {type}'")
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> stopping monitoring activities and rewards")
            await ctx.send(f"stopping monitoring at the end of the current period")
            self.monitoring_flag1 = False
            self.monitoring_flag2 = True

        # case : enable monitoring type
        if (keyword1.lower() == "enable"):

            # if monitoring type is none, cannot enable
            if (keyword2 == None):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{command}' (keyword2 argument missing)")
                await ctx.send("rejected command : invalid command arguments!")
                return

            # if monitoring type is not in monitorable types, invalid type
            if (keyword2 != None and isinstance(keyword2, str) and keyword2.lower() not in MONITORING_KEYWORDS_2_ENABLE):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{command}' (keyword2 argument invalid)")
                await ctx.send("rejected command : invalid command arguments!")
                return
            
            # if monitoring type is already enabled, cannot enable
            if (keyword2.lower() == "activities" and self.club9_bot.monitor_activities == True or keyword2.lower() == "rewards" and self.club9_bot.monitor_rewards == True):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{command}' (already enabled)")
                await ctx.send(f"rejected command : monitoring {keyword2.lower()} is already enabled")
                return

            # accept command
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> accepted user command '{command}'")
            if (keyword2.lower() == "activities"):
                self.club9_bot.monitor_activities = True
            elif (keyword2.lower() == "rewards"):
                self.club9_bot.monitor_rewards = True
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> enabled monitoring of {keyword2.lower()}")
            await ctx.send(f"enabled monitoring of type {keyword2.lower()}")

        # case : disable monitoring type
        if (keyword1.lower() == "disable"):

            # if monitoring type is none, cannot enable
            if (keyword2 == None):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{command}' (keyword2 argument missing)")
                await ctx.send("rejected command : invalid command arguments!")
                return

            # if monitoring type is not in monitorable types, invalid type
            if (keyword2 != None and isinstance(keyword2, str) and keyword2.lower() not in MONITORING_KEYWORDS_2_DISABLE):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{command}' (keyword2 argument invalid)")
                await ctx.send("rejected command : invalid command arguments!")
                return
            
            # if monitoring type is already enabled, cannot enable
            if (keyword2.lower() == "activities" and self.club9_bot.monitor_activities == False or keyword2.lower() == "rewards" and self.club9_bot.monitor_rewards == False):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{command}' (already enabled)")
                await ctx.send(f"rejected command : monitoring {keyword2.lower()} is already disabled")
                return

            # accept command
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> accepted user command '{command}'")
            if (keyword2.lower() == "activities"):
                self.club9_bot.monitor_activities = False
            elif (keyword2.lower() == "rewards"):
                self.club9_bot.monitor_rewards = False
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> disabled monitoring of {keyword2.lower()}")
            await ctx.send(f"disabled monitoring of type {keyword2.lower()}")

        # case : refresh specific monitoring type
        if (keyword1.lower() == "refresh"):

            # if monitoring type is none, cannot enable
            if (keyword2 == None):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{command}' (keyword2 argument missing)")
                await ctx.send("rejected command : invalid command arguments!")
                return

            # if monitoring type is not in monitorable types, invalid type
            if (keyword2 != None and isinstance(keyword2, str) and keyword2.lower() not in MONITORING_KEYWORDS_2_REFRESH):
                self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> rejected user command '{command}' (keyword2 argument invalid)")
                await ctx.send("rejected command : invalid command arguments!")
                return

            # accept command
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> accepted user command '{command}'")
            await ctx.send(f"refreshing {keyword2.lower()}")
            if (self.club9_bot.club9_cog_activities):
                await self.club9_bot.club9_cog_activities.refresh()
                self.club9_bot.num_activities_monitoring_cycles += 1
            if (self.club9_bot.club9_cog_rewards):
                await self.club9_bot.club9_cog_rewards.refresh()
                self.club9_bot.num_rewards_monitoring_cycles += 1
            self.club9_bot.logger.log(level=logging.INFO, msg=f"Club9Commands -> refreshed {keyword2.lower()}")
            await ctx.send(f"refreshed {keyword2.lower()}")


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
num_activities_monitoring_cycles = {self.club9_bot.num_activities_monitoring_cycles}
num_activities_monitoring_cycles = {self.club9_bot.num_rewards_monitoring_cycles}

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
