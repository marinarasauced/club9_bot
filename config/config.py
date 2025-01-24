
import datetime


def PATH_DISCORD_LOGS() -> str:
    """
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    return f"logs/discord_{timestamp}.log"


# .env
PATH_DOTENV = "../club9-bot-settings/.env"
DISCORD_TOKEN_NAME = "PROJETS_CLUB9_BOT_DISCORD_TOKEN"

# cookies
PATH_COOKIES = "../club9-bot-settings/cookies.txt"

# caches
PATH_ACTIVITIES_CACHE = "config/dict_activities.json"
PATH_MESSAGES_CACHE = "config/dict_messages.json"
PATH_REWARDS_CACHE = "config/dict_rewards.json"

# graphics
CLUB9_BOT_ICON_URL = "https://cdn.discordapp.com/attachments/1330310037968781363/1330659343841890345/club9-bot.png?ex=6794b756&is=679365d6&hm=a391c519254080dfaa3a641a9436f4f6581386c7b6ee7737b03559bce97d7ae3&"

# toki api
API_TOKI_ACTIVITIES_URL = "https://api.buildwithtoki.com/merchant/brand/activities"
API_TOKI_ACTIVITIES_PARAMS = None
API_TOKI_ACTIVITIES_HEADERS = {"x-shopify-shop-domain": "cloud9gg.myshopify.com",}

# rewards url
REWARDS_ELITE_URL = "https://store.cloud9.gg/collections/elite-tier-rewards"
REWARDS_MASTER_URL = "https://store.cloud9.gg/collections/master-tier-rewards"
REWARDS_CHAMPION_URL = "https://store.cloud9.gg/collections/champion-tier-rewards"
REWARDS_LEGENDARY_URL = "https://store.cloud9.gg/collections/legendary-tier-rewards"
REWARDS_MYTHIC_URL = "https://store.cloud9.gg/collections/mythic-tier-rewards"

REWARDS_ELITE_SEARCH_STRING = "/collections/elite-tier-rewards/products/"
REWARDS_MASTER_SEARCH_STRING = "/collections/master-tier-rewards/products/"
REWARDS_CHAMPION_SEARCH_STRING = "/collections/champion-tier-rewards/products/"
REWARDS_LEGENDARY_SEARCH_STRING = "/collections/legendary-tier-rewards/products/"
REWARDS_MYTHIC_SEARCH_STRING = "/collections/mythic-tier-rewards/products/"

REWARDS_QUERY_URL = "https://store.cloud9.gg/search?type=product&view=sc-pb-front-25052016&q="

# discord notifications
DISCORD_CHANNEL_ID_CLUB9_NOTIFICATIONS = 1330410207376838737
DISCORD_ROLE_ID_CLUB9_NOTIFICATIONS = 1328430817214599370

# discord rewards
DISCORD_CHANNEL_ID_CLUB9_REWARDS_ELITE = 1330686037243986074
DISCORD_CHANNEL_ID_CLUB9_REWARDS_MASTER = 1330686452673150976
DISCORD_CHANNEL_ID_CLUB9_REWARDS_CHAMPION = 1330686482066833460
DISCORD_CHANNEL_ID_CLUB9_REWARDS_LEGENDARY = 1330686526828445856
DISCORD_CHANNEL_ID_CLUB9_REWARDS_MYTHIC = 1330686616624431217

# discord diagnostics
DISCORD_CHANNEL_ID_CLUB9_BOT_LOGS = 1330310063482732614
DISCORD_CHANNEL_ID_CLUB9_BOT_COMMANDS = 1330310094524518480

# bot settings
NOTIFICATIONS_ACTIVITIES_ENABLE_URLS = True
NOTIFICATIONS_ACTIVITIES_URL = "https://store.cloud9.gg/pages/club9"
NOTIFICATIONS_REWARDS_ENABLE_URLS = True
DISCORD_COMMAND_PREFIX = "!"

ENABLE_MONITORING_ON_STARTUP_BOOL = True
ENABLE_MONITORING_ON_STARTUP_PERIOD = 600

ENABLE_MONITORING_ACTIVITIES_ON_STARTUP_BOOL = True
ENABLE_MONITORING_REWARDS_ON_STARTUP_BOOL = True