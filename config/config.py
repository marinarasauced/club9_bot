
import datetime

# API_URL_SETTINGS = "https://api.buildwithtoki.com/ui-modules/settings?shop_domain=cloud9gg.myshopify.com&type=activities"
# API_URL_SETTINGS_IDS = [
#     "a3a263e0-5b53-4b66-8490-2f3ec8bff9bd",
#     "e2780a78-1052-4f4b-854e-b2cce90934e1",
#     "de7e84d0-e670-4e0e-8769-cda3197f3f92",
#     "efc1371b-add1-4cca-9bc6-dfd9e7cb596c",
#     "11cbc8d1-10a3-410e-8e70-63e58e76e608",
# ]
# API_URL_ACTIVITIES = "https://api.buildwithtoki.com/merchant/brand/activities"
# API_URL_ACTIVITIES_HEADERS = {
#     "x-shopify-shop-domain": "cloud9gg.myshopify.com",
# }1328210209088475280
# DISCORD_CHANNEL_ID_TESTING = 1328209261632950303
# DISCORD_CHANNEL_ID_LOGGING = 
# DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS = 1328430817214599370
# PATH_CACHE_API_ACTIVITIES = "config/api_activities.json"


def PATH_DISCORD_LOGS() -> str:
    """
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    return f"logs/discord_{timestamp}.log"


# .env
PATH_DOTENV = "../.env"
DISCORD_TOKEN_NAME = "PROJETS_CLUB9_BOT_DISCORD_TOKEN"

# graphics
CLUB9_BOT_ICON_URL = "https://1000logos.net/wp-content/uploads/2017/08/Logo-Cloud-9.jpg"

# toki api
API_TOKI_ACTIVITIES_URL = "https://api.buildwithtoki.com/merchant/brand/activities"
API_TOKI_ACTIVITIES_PARAMS = None
API_TOKI_ACTIVITIES_HEADERS = {"x-shopify-shop-domain": "cloud9gg.myshopify.com",}
PATH_TOKI_ACTIVITIES_CACHE = "config/activities_dict.json"

# discord notifications
DISCORD_CHANNEL_ID_CLUB9_NOTIFICATIONS = 1330410207376838737
DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS = 1328430817214599370

# discord diagnostics
DISCORD_CHANNEL_ID_CLUB9_BOT_LOGS = 1330310063482732614
DISCORD_CHANNEL_ID_CLUB9_BOT_COMMANDS = 1330310094524518480

# bot settings
NOTIFICATIONS_ACTIVITIES_ENABLE_URLS = True
NOTIFICATIONS_ACTIVITIES_URL = "https://store.cloud9.gg/pages/club9"
