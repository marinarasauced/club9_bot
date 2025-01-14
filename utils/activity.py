
from enum import Enum
from typing import Any, List, Optional


class Club9ActivityType(Enum):
    """
    This class provides several enum used to differentiate activity types.
    """
    QUEST_INTERNAL = 0      # Users complete the activity on the 'https://store.cloud9.gg/pages/club9' page.
    QUEST_EXTERNAL = 1      # Users complete the activity external to the 'https://store.cloud9.gg/pages/club9' page.
    CHALLENGE = 2           # Users complete the activity by completing several quests.
    NONE = 3                # A placeholder value for quests that have not yet been loaded.


class Club9ActivityData():
    """
    This class provides methods to define the attributes depending on the activity type.
    """
    def __init__(self, data: dict[str, Any]):
        """
        Initializes the Club9 Activity
        """
        self.club9_activity_type = Club9ActivityType.NONE
        # TODO add logic to decompose the data input, identify the activity type, and assign the object a type with the corresponding method


    def flatten(self, d: dict[str, Any], parent: str = "", separator: str = "_") -> dict[str, Any]:
        """
        Flattens a dictionary.

        @param d: The dictionary data to flatten.
        @param parent: The parent key to append to the child key names.
        @param separator: The character used to separate the parent and child in the new key names.
        @return: A flattened version of the input data.
        """
        items = []
        for k, v in d.items():
            key = f"{parent}{separator}{k}" if parent else k
            if isinstance(v, dict):
                items.extend(self.flatten(v, key, separator=separator).items())
            else:
                items.append((key, v))
        return dict(items)


    def quest_internal(self, data: dict):
        """
        Defines the activity as an internal quest
        """

