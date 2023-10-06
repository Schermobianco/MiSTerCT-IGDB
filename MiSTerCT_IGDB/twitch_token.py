import os
import requests
from dotenv import load_dotenv


# load the needed env vars.
# order is: os env first, .env file second. (see https://pypi.org/project/python-dotenv/)
load_dotenv(override=False)

TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET")
TWITCH_AUTH_ENDPOINT = "https://id.twitch.tv/oauth2/token"


def get_access_token():
    try:
        auth_body = {
            "client_id": TWITCH_CLIENT_ID,
            "client_secret": TWITCH_CLIENT_SECRET,
            "grant_type": "client_credentials",
        }
        auth_response = requests.post(TWITCH_AUTH_ENDPOINT, auth_body)
        auth_response.raise_for_status()
        return auth_response.json()["access_token"]
    except Exception as e:
        print(f"<Error! - TOKEN> {e}")
        return None


if __name__ == "__main__":
    access_token = get_access_token()
    print(access_token)
