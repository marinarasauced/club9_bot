
import datetime

API_URL_SETTINGS = "https://api.buildwithtoki.com/ui-modules/settings?shop_domain=cloud9gg.myshopify.com&type=activities"
API_URL_SETTINGS_IDS = [
    "a3a263e0-5b53-4b66-8490-2f3ec8bff9bd",
    "e2780a78-1052-4f4b-854e-b2cce90934e1",
    "de7e84d0-e670-4e0e-8769-cda3197f3f92",
    "efc1371b-add1-4cca-9bc6-dfd9e7cb596c",
    "11cbc8d1-10a3-410e-8e70-63e58e76e608",
]
API_URL_ACTIVITIES = "https://api.buildwithtoki.com/merchant/brand/activities"
API_URL_ACTIVITIES_HEADERS = {
    "x-shopify-shop-domain": "cloud9gg.myshopify.com",
}
DISCORD_CHANNEL_ID_TESTING = 1328209261632950303
DISCORD_CHANNEL_ID_LOGGING = 1328210209088475280
DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS = 1328430817214599370
PATH_CACHE_API_ACTIVITIES = "config/api_activities.json"


def PATH_DISCORD_LOGS() -> str:
    """
    """
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    return f"logs/discord_{timestamp}.log"







API_TOKI_ACTIVITIES_URL = "https://api.buildwithtoki.com/merchant/brand/activities"
API_TOKI_ACTIVITIES_PARAMS = None
API_TOKI_ACTIVITIES_HEADERS = {"x-shopify-shop-domain": "cloud9gg.myshopify.com",}
PATH_TOKI_ACTIVITIES_CACHE = "config/activities.json"