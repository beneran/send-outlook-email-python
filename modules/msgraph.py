from msal import PublicClientApplication, SerializableTokenCache
import webbrowser
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
SCOPES = ["Mail.Send"]

authority_url = "https://login.microsoftonline.com/consumers/"


def get_token_cache(token_file):
    acces_token_cache = SerializableTokenCache()
    if os.path.exists(token_file):
        acces_token_cache.deserialize(open(token_file, "r").read())
        token_detail = json.load(open(token_file, "r"))
        token_detail_key = list(token_detail["AccessToken"].keys())[0]
        token_expiration = datetime.fromtimestamp(
            int(token_detail["AccessToken"][token_detail_key]["expires_on"])
        )
        if datetime.now() > token_expiration:
            os.remove(token_file)
            acces_token_cache = SerializableTokenCache()
    return acces_token_cache


def get_access_token():
    print(APP_ID)
    stored_token_path = os.path.join("token", "api_token.json")
    acces_token_cache = get_token_cache(stored_token_path)

    app = PublicClientApplication(
        APP_ID, authority=authority_url, token_cache=acces_token_cache
    )

    accounts = app.get_accounts()
    if accounts:
        token_response = app.acquire_token_silent(SCOPES, accounts[0])["access_token"]
    else:
        flow = app.initiate_device_flow(scopes=SCOPES)
        print(flow)
        webbrowser.open("https://www.microsoft.com/link")
        result = app.acquire_token_by_device_flow(flow)

        token_response = result["access_token"]

    with open(stored_token_path, "w") as _f:
        _f.write(acces_token_cache.serialize())

    print(token_response)
    return token_response


if __name__ == "__main__":
    get_access_token()
