
import requests
import json


def fetch_api_data(url: str | bytes, params: dict = None, headers: dict = None):
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


url = "https://api.buildwithtoki.com/merchant/brand/activities"
params = {"reward_rule_id": "8d974481-f5e7-459e-9a90-3c6bfd9eef7c"}
headers = {"x-shopify-shop-domain": "cloud9gg.myshopify.com",}

with open("test3.json", "w") as file:
    json.dump(fetch_api_data(url=url, params=None, headers=headers), file, indent=4)
