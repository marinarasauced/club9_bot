
from config.config import *
import discord
import logging
import random
import requests


class APIClient:
    """
    """
    def __init__(self, logger=logging.getLogger("discord")):
        """
        """
        self.logger = logger


    class Setting:
        """
        """
        def __init__(self, data: dict, key: str):
            """
            """
            self.data = data
            self.key = key
            self.unpack(data=data.get("data", {}))


        def show(self):
            """
            """
            for attr, value in self.__dict__.items():
                print(f"{attr}: {value}")


        def unpack(self, data: dict):
            """
            """
            # self.setting_id = data.get("setting_id")
            # self.created_at = data.get("created_at")
            # self.updated_at = data.get("updated_at")
            # self.deleted_at = data.get("deleted_at")
            # self.is_publish = data.get("is_publish")
            # self.merchant_id = data.get("merchant_id")
            # self.module_type = data.get("module_type")
            # self.name = data.get("name")

            settings = data.get("settings", {})
            # self.is_shadow_root = settings.get("isShadowRoot")
            self.activity_ids = settings.get("activityIds", [])
            # self.section_vertical_padding = settings.get("sectionVerticalPadding")
            # self.section_horizontal_padding = settings.get("sectionHorizontalPadding")
            # self.hide_already_done_activities = settings.get("hideAlreadyDoneActivities")
            # self.activities_all_completed_text = settings.get("activitiesAllCompletedText")
            # self.activities_all_completed_size = settings.get("activitiesAllCompletedSize")
            # self.activities_all_completed_font_weight = settings.get("activitiesAllCompletedFontWeight")
            # self.is_end_activity_on_external_page = settings.get("isEndActivityOnExternalPage")
            self.header_title = settings.get("headerTitle")
            # self.header_color = settings.get("headerColor")
            # self.header_size = settings.get("headerSize")
            # self.header_font_weight = settings.get("headerFontWeight")
            # self.first_row_text_color = settings.get("firstRowTextColor")
            # self.first_row_text_size = settings.get("firstRowTextSize")
            # self.first_row_order_number = settings.get("firstRowOrderNumber")
            # self.second_row_text_size = settings.get("secondRowTextSize")
            # self.second_row_order_number = settings.get("secondRowOrderNumber")
            # self.third_row_text_color = settings.get("thirdRowTextColor")
            # self.third_row_text_size = settings.get("thirdRowTextSize")
            # self.third_row_order_number = settings.get("thirdRowOrderNumber")
            # self.rows_gap = settings.get("rowsGap")
            # self.completed_with_limit_message = settings.get("completedWithLimitMessage")
            # self.completed_without_limit_message = settings.get("completedWithoutLimitMessage")
            # self.completed_with_pending_approval_message = settings.get("completedWithPendingApprovalMessage")
            # self.paging_dots_color = settings.get("pagingDotsColor")
            # self.slides_to_show = settings.get("slidesToShow")
            # self.block_background_color = settings.get("blockBackgroundColor")
            # self.block_border_color = settings.get("blockBorderColor")
            # self.block_border_width = settings.get("blockBorderWidth")
            # self.block_border_radius = settings.get("blockBorderRadius")
            # self.hide_button = settings.get("hideButton")
            # self.block_button_text = settings.get("blockButtonText")
            # self.block_button_login_text = settings.get("blockButtonLoginText")
            # self.block_button_login_url = settings.get("blockButtonLoginUrl")
            # self.block_button_background = settings.get("blockButtonBackground")
            # self.block_button_text_color = settings.get("blockButtonTextColor")
            # self.block_button_border_color = settings.get("blockButtonBorderColor")
            # self.block_button_border_width = settings.get("blockButtonBorderWidth")
            # self.block_button_text_size = settings.get("blockButtonTextSize")
            # self.block_button_position = settings.get("blockButtonPosition")
            # self.block_button_border_radius = settings.get("blockButtonBorderRadius")
            # self.block_button_text_transform = settings.get("blockButtonTextTransform")
            # self.activity_image_display_type = settings.get("activityImageDisplayType")
            # self.activity_image_position = settings.get("activityImagePosition")
            # self.activity_icon_display_type = settings.get("activityIconDisplayType")
            # self.activity_icon_width = settings.get("activityIconWidth")
            # self.mobile_layout_activities_per_row = settings.get("mobileLayoutActivitiesPerRow")
            # self.mobile_layout_slider_show_arrows = settings.get("mobileLayoutSliderShowArrows")
            # self.slider_arrow_color = settings.get("sliderArrowColor")
            # self.slider_arrow_background_color = settings.get("sliderArrowBackgroundColor")
            # self.slider_arrow_border_radius = settings.get("sliderArrowBorderRadius")
            # self.slider_arrow_size = settings.get("sliderArrowSize")
            # self.slider_next_button_text = settings.get("sliderNextButtonText")
            # self.slider_prev_button_text = settings.get("sliderPrevButtonText")
            # self.mobile_layout_slider_show_dots = settings.get("mobileLayoutSliderShowDots")
            # self.language = settings.get("language")
            # self.custom_css = settings.get("customCss")


    class Activity:
        """
        Represents an activity with associated attributes.
        """

        def __init__(self, data: dict, key: str):
            """
            """
            self.data = data
            self.key = key
            if (len(data.get("activities")) == 1):
                self.unpack(data.get("activities")[0])

        def show(self):
            """
            """
            for attr, value in self.__dict__.items():
                print(f"{attr}: {value}")

        def unpack(self, data: dict):
            """
            """
            self.id = data.get("id")
            self.name = data.get("name")
            # self.description = data.get("description")
            # self.url = data.get("url")
            self.image = data.get("image")
            # self.icon_image = data.get("iconImage")
            # self.custom = data.get("custom")
            # self.reward_message = data.get("rewardMessage")
            # self.completed = data.get("completed")
            # self.limit_reached = data.get("limitReached")
            # self.pending_review = data.get("pendingReview")
            # self.automatically_approve = data.get("automaticallyApprove")
            # self.retroactive_submission = data.get("retroactiveSubmission")
            # self.max_files_limit = data.get("maxFilesLimit")
            # self.type_identifier = data.get("typeIdentifier")
            self.completions_limit = data.get("completionsLimit", {})
            # self.products = data.get("products")

            additional_fields = data.get("additionalFields", {})
            # self.additional_fields_shop_ids = additional_fields.get("shopIds", [])
            # self.additional_fields_reward_name = additional_fields.get("rewardName")
            # self.additional_fields_description = additional_fields.get("description")
            # self.additional_fields_display_rule = additional_fields.get("displayRule", {})
            # self.additional_fields_button_settings = additional_fields.get("buttonSettings", {})
            # self.additional_fields_is_one_time_reward = additional_fields.get("isOneTimeReward")
            # self.additional_fields_visibility_settings = additional_fields.get("visibilitySettings", {})
            # self.additional_fields_image = additional_fields.get("image")
            self.additional_fields_closed_at = additional_fields.get("closed_at")
            # self.additional_fields_icon_image = additional_fields.get("iconImage")
            self.additional_fields_started_at = additional_fields.get("started_at")
            # self.additional_fields_prevent_re_submissions = additional_fields.get("preventReSubmissions")

            reward = data.get("reward", {})
            # self.reward_rule_id = reward.get("reward_rule_id")
            # self.reward_activity_id = reward.get("activity_id")
            # self.reward_type = reward.get("reward_type")
            # self.reward_asset_to_reward_id = reward.get("asset_to_reward_id")
            self.reward_amount_to_reward = reward.get("amount_to_reward")
            # self.reward_amount_to_reward_percentage = reward.get("amount_to_reward_percentage")
            # self.reward_product_variant_id = reward.get("product_variant_id")
            # self.reward_discount_absolute = reward.get("discount_absolute")
            # self.reward_discount_percent = reward.get("discount_percent")
            # self.reward_segment_id = reward.get("segment_id")
            # self.reward_order_number = reward.get("order_number")
            # self.reward_additional_fields = reward.get("additional_fields", {})
            # self.reward_tier_id = reward.get("tier_id")
            # self.reward_product_variant_ids = reward.get("product_variant_ids")
            # self.reward_token_name = reward.get("token_name")
            # self.reward_token_id = reward.get("token_id")
            # self.reward_image_url = reward.get("image_url")
            # self.reward_shopify_product_variant_label = reward.get("shopify_product_variant_label")


    def fetch_api_data(self, url: str | bytes, params: dict = None, headers: dict = None):
        """
        Fetch data from the given API URL.

        @param url: The HTTPS URL of the API.
        @param params: Augments of the URL"s query string.
        @param headers: HTTP headers to add to the request.
        @return: A JSON dictionary if successful, otherwise None.
        """
        try:
            response = requests.get(url=url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            print(error)
            return None
        

    def fetch_api_settings(self, setting_ids: list[str]):
        """
        """
        settings = []
        for setting_id in setting_ids:
            url = f"{API_URL_SETTINGS}&setting_id={setting_id}"
            data = self.fetch_api_data(url=url, params=None, headers=None)
            setting = self.Setting(data=data, key=setting_id)
            self.logger.log(level=logging.INFO, msg=f"\tfetched data for settings key {setting_id}")
            settings.append(setting)
        return settings


    def fetch_api_activities(self, settings: list[Setting]):
        """
        """
        activities = {}
        for setting in settings:
            for activity_id in setting.activity_ids:
                url = API_URL_ACTIVITIES
                params = {"activityIds": [activity_id]}
                headers = API_URL_ACTIVITIES_HEADERS
                data = self.fetch_api_data(url=url, params=params, headers=headers)
                activity = self.Activity(data=data, key=activity_id)
                self.logger.log(level=logging.INFO, msg=f"\tfetched data for activities key {activity_id}")
                activities[activity_id] = activity
        return activities


    def generate_api_activity_content(self):
        """
        """
        messages = [
            f"<@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>, a new quest has been posted!",
            f"<@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>, a fresh quest is now live!",
            f"A new quest has arrived <@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>!",
            f"<@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>, a brand new quest is now available!",
            f"<@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>, a new quest has been added!",
            f"New quest alert <@&{DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS}>!",
        ]
        content = random.choice(messages)
        return content


    def generate_api_activity_embed(self, activity: Activity):
        """
        """
        activity_name = activity.name
        activity_reward = activity.reward_amount_to_reward
        try:
            activity_reward = f"Reward {int(activity_reward)} XP"
        except:
            activity_reward = activity_reward
        embed = discord.Embed(
            title=activity_name,
            description=activity_reward,
            color=discord.Color.blue(),
        )
        embed.set_image(url=activity.image)
        return embed
    

        # has_additional_fields_started_at = hasattr(activity, "additional_fields_started_at")
        # has_additional_fields_closed_at = hasattr(activity, "additional_fields_closed_at")
        # is_timed = False
        # if (has_additional_fields_started_at and has_additional_fields_closed_at):
        #     if (activity.additional_fields_started_at != None and activity.additional_fields_closed_at != None):
        #         is_timed = True