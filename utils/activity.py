
import datetime
import discord
from enum import Enum
import random
from typing import Any

from config.config import (
    DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS,
    CLUB9_BOT_ICON_URL,
    NOTIFICATIONS_ACTIVITIES_ENABLE_URLS,
    NOTIFICATIONS_ACTIVITIES_URL,
)


class Club9ActivityType(Enum):
    """
    This class provides several enum used to differentiate activity types.

    The default enum is labeled as QUEST_INTERNAL, and in this case, if a notification were to be sent, the only information included are the name, description, and image from the quest data from the api. Challenges include a field in the embed where all required quest names are listed in order to complete the challenge. External quests (i.e., video quests) TODO ...
    """
    NONE = None                                     # A placeholder value for quests that have not yet been loaded.
    CHALLENGE = "CHALLENGE"                         # Users complete the activity by completing several quests.
    QUEST_EXTERNAL = "NON_INTEGRATION_CUSTOM"       # Users complete the activity external to the 'https://store.cloud9.gg/pages/club9' page.
    QUEST_INTERNAL = "DEFAULT"                      # Users complete the activity on the 'https://store.cloud9.gg/pages/club9' page.
    # HIDDEN = "HIDDEN"                               # 


    @classmethod
    def _missing_(cls, value):
        """
        Unknown values are mapped to 'QUEST_INTERNAL' as a fallback.
        
        @param cls:
        @param value:
        """
        return cls.QUEST_INTERNAL


class Club9ActivityData():
    """
    This class takes an activity's dictionary, decomposes it to assign each key as an attribute equal to the respective value, and determines the activity's type using the activity type enum.
    """
    def __init__(self, data: dict[str, Any]):
        """
        Initializes the Club9 Activity
        """
        self.club9_activity_data = data
        for k, v in self.get_activity_data(data=self.club9_activity_data).items():
            setattr(self, k, v)
        self.club9_activity_type = self.get_activity_type()


    def show(self) -> None:
        """
        Prints all attributes to the terminal.
        """
        for attr, value in self.__dict__.items():
            print(f"{attr}: {value}")


    def get_activity_data(self, data: dict[str, Any], parent: str = "", separator: str = "_") -> dict[str, Any]:
        """
        Gets the formatted activity data by flattening the activity dict.

        @param data: The dictionary data to flatten.
        @param parent: The parent key to append to the child key names.
        @param separator: The character used to separate the parent and child in the new key names.
        @return: A flattened version of the input data.
        """
        items = []
        for k, v in data.items():
            key = f"{parent}{separator}{k}" if parent else k
            if isinstance(v, dict):
                items.extend(self.get_activity_data(v, key, separator=separator).items())
            else:
                items.append((key, v))
        return dict(items)


    def get_activity_type(self) -> Club9ActivityType:
        """
        Gets the activity type by analyzing the activity data.
        """
        if (hasattr(self, "typeIdentifier") == False or hasattr(self, "id") == False):
            return Club9ActivityType(None)
        else:
            return Club9ActivityType(self.typeIdentifier)


    def generate_activities_content(self) -> str:
        """
        Generates the text component of the discord notification for a new activity including a role ping and a short indication that there is a new quest/challenge.

        @return: The 'content' string for the discord bot to publish in the notification message.
        """
        activity_type = ""
        if (self.club9_activity_type == Club9ActivityType.CHALLENGE):
            activity_type = "challenge"
        elif (self.club9_activity_type == Club9ActivityType.QUEST_INTERNAL or self.club9_activity_type == Club9ActivityType.QUEST_EXTERNAL):
            activity_type = "quest"
        messages = [
            f"<@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>, a new {activity_type} has been posted!",
            f"<@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>, a fresh {activity_type} is now live!",
            f"A new {activity_type} has arrived <@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>!",
            f"<@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>, a brand new {activity_type} is now available!",
            f"<@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>, a new {activity_type} has been added!",
            f"New {activity_type} alert <@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>!",
        ]
        content = random.choice(messages)
        return content


    def generate_activities_embed(self) -> discord.Embed:
        """
        Generates the discord embed of the discord notification for a new activity including a name, reward, image, visibility, start/stop times if applicable, etc.
        """
        embed = discord.Embed()
        embed.color = discord.Color.blue()                      # default color
        embed.title = self.name                                 # set name by default
        embed.set_image(url=self.image)                         # set image by default
        
        # add url to embed title linking to cloud9 club9 activities page
        if (NOTIFICATIONS_ACTIVITIES_ENABLE_URLS == True):
            embed.url = NOTIFICATIONS_ACTIVITIES_URL

        # set author, icon, description
        embed.set_author(name="Challenge" if self.club9_activity_type == Club9ActivityType.CHALLENGE else "Quest", icon_url=CLUB9_BOT_ICON_URL)

        # add reward amount if available
        if (self.rewardMessage != None and self.rewardMessage != ""):
            try:
                embed.add_field(
                    name="Reward",
                    value=f"{self.rewardMessage}",
                    inline=False,
                )
            except:
                pass

        # add expiration date if applicable
        if (self.additionalFields_closed_at != None and self.additionalFields_closed_at != ""):
            try:
                stamp_dt = datetime.datetime.fromisoformat(self.additionalFields_closed_at.replace("Z", "+00:00"))
                stamp_unix = int(stamp_dt.timestamp())
                stamp_discord = f"<t:{stamp_unix}>"
                embed.add_field(
                    name="Claimable Until",
                    value=stamp_discord,
                    inline=False,
                )
            except:
                pass

        # if challenge, add required quests
        if (self.club9_activity_type == Club9ActivityType.CHALLENGE):
            try:
                embed.add_field(
                    name="Quests", 
                    value="\n".join(activity.get("label", "") for activity in self.additionalFields_challenges_activities),
                    inline=False,
                )
            except:
                pass


        # if video quest, add watch time requirement and active range
        # TODO scrape other api for watch requirement data

        #
        if self.club9_activity_type == Club9ActivityType.NONE:
            return None
        return embed


def generate_activities(activities_list: list) -> dict[str, Club9ActivityData]:
    """
    Generates a dict of Club9ActivityData objects from a list of activity dictionaries.

    @param activities: A list of activity dictionaries from the activities query results after getting 'activities'.
    @return: A list of Club9ActivityData objects.
    """
    # TODO add detection for visibility (in case of hidden quests, no need to ping users)
    activities_data = {}
    for activity_dict in activities_list:
        activity_data = Club9ActivityData(data=activity_dict)
        if (hasattr(activity_data, "additionalFields_visibilitySettings_type") == True):
            if (activity_data.additionalFields_visibilitySettings_type != "all_users"):
                activity_data.club9_activity_type = Club9ActivityType.NONE
        if (hasattr(activity_data, "id") == True and (activity_data.id != None and activity_data.id != "")):
            activities_data[activity_data.id] = activity_data
    return activities_data
