
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
