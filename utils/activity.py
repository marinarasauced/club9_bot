
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
        self.club9_activity_data = data
        for k, v in self.get_activity_data(data=self.club9_activity_data).items():
            setattr(self, k, v)
        self.club9_activity_type = Club9ActivityType.NONE
        # TODO add logic to decompose the data input, identify the activity type, and assign the object a type with the corresponding method


    def show(self):
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


    def get_activity_type(self):
        """
        Gets the activity type by analyzing the activity data.
        """


    def quest_internal(self, data: dict):
        """
        Defines the activity as an internal quest
        """






















test = {
    "id": "18111518-18f3-43e8-a96d-0b3d4e66effb",
    "name": "[VAL] Watch C9 vs NRG - VCT Americas Kickoff",
    "description": "",
    "url": "",
    "image": "https://s3.buildwithtoki.com/files/v0/sandbox/79990613-eac4-4477-bb3e-93b4a46a2958.png",
    "iconImage": "",
    "rewardMessage": "XP",
    "additionalFields": {
        "shopIds": [],
        "rewardName": "",
        "description": "",
        "displayRule": {
            "name": "[VAL] Watch C9 vs NRG - VCT Americas Kickoff",
            "image": "https://s3.buildwithtoki.com/files/v0/sandbox/79990613-eac4-4477-bb3e-93b4a46a2958.png",
            "custom": False,
            "iconImage": "",
            "description": ""
        },
        "buttonSettings": {
            "enabled": False
        },
        "isOneTimeReward": True,
        "visibilitySettings": {
            "type": "all_users"
        },
        "image": "https://s3.buildwithtoki.com/files/v0/sandbox/79990613-eac4-4477-bb3e-93b4a46a2958.png",
        "closed_at": "2025-01-18T06:00:36.930Z",
        "iconImage": "",
        "started_at": None,
        "externalUrl": "https://store.cloud9.gg/pages/video?slug=vct-americas-kickoff-c9-vs-nrg",
        "preventReSubmissions": False
    },
    "reward": {
        "reward_rule_id": "8d974481-f5e7-459e-9a90-3c6bfd9eef7c",
        "activity_id": "18111518-18f3-43e8-a96d-0b3d4e66effb",
        "reward_type": "asset",
        "asset_to_reward_id": "6e23ba5d-868e-496e-bc80-ba8f75e671e0",
        "amount_to_reward": None,
        "amount_to_reward_percentage": None,
        "product_variant_id": None,
        "discount_absolute": None,
        "discount_percent": None,
        "segment_id": None,
        "order_number": 0,
        "additional_fields": {
            "shopIds": [],
            "rewardName": "",
            "description": "",
            "displayRule": {
                "name": "[VAL] Watch C9 vs NRG - VCT Americas Kickoff",
                "image": "https://s3.buildwithtoki.com/files/v0/sandbox/79990613-eac4-4477-bb3e-93b4a46a2958.png",
                "custom": False,
                "iconImage": "",
                "description": ""
            },
            "buttonSettings": {
                "enabled": False
            },
            "isOneTimeReward": True,
            "visibilitySettings": {
                "type": "all_users"
            }
        },
        "tier_id": None,
        "product_variant_ids": None,
        "token_name": "XP",
        "token_id": "6e23ba5d-868e-496e-bc80-ba8f75e671e0",
        "image_url": None,
        "shopify_product_variant_label": None
    },
    "completed": False,
    "limitReached": False,
    "pendingReview": False,
    "automaticallyApprove": True,
    "retroactiveSubmission": False,
    "maxFilesLimit": None,
    "typeIdentifier": "NON_INTEGRATION_CUSTOM",
    "completionsLimit": {
        "type": "unlimited"
    },
    "products": None
}


idk = Club9ActivityData(test)
idk.show()