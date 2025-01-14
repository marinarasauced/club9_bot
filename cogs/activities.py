
from enum import Enum


class Club9ActivityType(Enum):
    """
    This class provides several enum used to differentiate activity types.
    """
    QUEST_INTERNAL = 0      # Users complete the activity on the 'https://store.cloud9.gg/pages/club9' page.
    QUEST_EXTERNAL = 1      # Users complete the activity external to the 'https://store.cloud9.gg/pages/club9' page.
    CHALLENGE = 2           # Users complete the activity by completing several quests.
    NONE = 3                # A placeholder value for quests that have not yet been loaded.


class Club9Activity():
    """
    This class provides a structure to map and store data from the TOKI API activity requests for use in methods external to this utils file.
    """
    def __init__(self):
        """
        Initializes the Club9 activity.
        """
        self.club9_activity_type = Club9ActivityType.NONE
