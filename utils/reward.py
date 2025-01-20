
from config.config import *
import discord
from enum import Enum


class Club9RewardType(Enum):
    """
    This class provides several enum used to differentiate reward types.
    """
    NONE = None                                     # Default enum value.
    ELITE = "ELITE"                                 # Elite Tier Rewards.
    MASTER = "MASTER"                               # Master Tier Rewards.
    CHAMPION = "CHAMPION"                           # Champion Tier Rewards.
    LEGENDARY = "LEGENDARY"                         # Legendary Tier Rewards.
    MYTHIC = "MYTHIC"                               # Mythic Tier Rewards.


    @classmethod
    def _missing_(cls, value):
        """
        Unknown values are mapped to 'NONE' as a fallback.
        
        @param cls:
        @param value:
        """
        return cls.NONE


def get_reward_types() -> list[str]:
    """
    Gets the reward types from the Club9Reward Enum class.
    """
    rewards_types = []
    for reward_type in Club9RewardType.__members__.values():
        if (reward_type is not Club9RewardType.NONE):
            rewards_types.append(reward_type.value)
    return rewards_types


def get_reward_channel_id(category: Club9RewardType) -> int:
    """
    Gets the discord channel id for the respective reward category.

    @param category: The Club9 reward category.
    @return: The channel id if category is valid, otherwise None.
    """
    if (category == Club9RewardType.ELITE or Club9RewardType(category) == Club9RewardType.ELITE):
        return DISCORD_CHANNEL_ID_CLUB9_REWARDS_ELITE
    elif (category == Club9RewardType.MASTER or Club9RewardType(category) == Club9RewardType.MASTER):
        return DISCORD_CHANNEL_ID_CLUB9_REWARDS_MASTER
    elif (category == Club9RewardType.CHAMPION or Club9RewardType(category) == Club9RewardType.CHAMPION):
        return DISCORD_CHANNEL_ID_CLUB9_REWARDS_CHAMPION
    elif (category == Club9RewardType.LEGENDARY or Club9RewardType(category) == Club9RewardType.LEGENDARY):
        return DISCORD_CHANNEL_ID_CLUB9_REWARDS_LEGENDARY
    elif (category == Club9RewardType.MYTHIC or Club9RewardType(category) == Club9RewardType.MYTHIC):
        return DISCORD_CHANNEL_ID_CLUB9_REWARDS_MYTHIC
    else:
        return None


def generate_reward_embed(reward_data, category) -> discord.Embed:
    """
    Generates the discord embed for a Club9 shop item including stock, prices, variants, item image, etc.
    """
    try:
        embed = discord.Embed()
        embed.color = discord.Color.blue()
        embed.title = reward_data.get("title")
        embed.set_thumbnail(url="https:" + reward_data["image"]["src"])
        if (NOTIFICATIONS_REWARDS_ENABLE_URLS == True):
            url = "https://store.cloud9.gg/collections/" + category.lower() + "-tier-rewards/products/" + reward_data["handle"]
            embed.url = url
        variants = reward_data["variants"]
        if (len(variants) == 0):
            return None
        elif (len(variants) == 1):
            variant = variants[0]
            embed.add_field(
                name=f"",
                value=f"""
Price: {variant['price']} XP
Stock: {variant['inventory_quantity']} available
                """,
                inline=False
            )
        elif (len(variants) > 1):
            for variant in reward_data['variants']:
                embed.add_field(
                    name=f"{variant['title']}",
                    value=(
                        f"Price: {variant['price']} XP\n"
                        f"Stock: {variant['inventory_quantity']} available\n"
                    ),
                    inline=False
                )
        return embed
    except Exception as e:
        return None
