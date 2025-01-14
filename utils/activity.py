
from enum import Enum
from typing import Any


class Club9ActivityType(Enum):
    """
    This class provides several enum used to differentiate activity types.
    """
    NONE = None                                     # A placeholder value for quests that have not yet been loaded.
    CHALLENGE = "CHALLENGE"                         # Users complete the activity by completing several quests.
    QUEST_EXTERNAL = "NON_INTEGRATION_CUSTOM"       # Users complete the activity external to the 'https://store.cloud9.gg/pages/club9' page.
    QUEST_INTERNAL = "DEFAULT"                      # Users complete the activity on the 'https://store.cloud9.gg/pages/club9' page.


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

        @param d: The dictionary data to flatten.
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


def generate_activities(activities_list: list) -> list[Club9ActivityData]:
    """
    Generates a list of Club9ActivityData objects from a list of activity dictionaries.

    @param activities: A list of activity dictionaries from the activities query results after getting 'activities'.
    @return: A list of Club9ActivityData objects.
    """
    activities_data = []
    for activity_dict in activities_list:
        activity_data = Club9ActivityData(data=activity_dict)
        activities_data.append(activity_data)
    return activities_data
