import requests
import os

def get_access_token():
    url = "https://accounts.zoho.in/oauth/v2/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("ZOHO_CLIENT_ID"),
        "client_secret": os.getenv("ZOHO_CLIENT_SECRET"),
        "refresh_token": os.getenv("ZOHO_REFRESH_TOKEN")
    }

    response = requests.post(url, data=payload)

    print("Token Status:", response.status_code)
    print("Token Response:", response.text)

    data = response.json()

    if "access_token" not in data:
        raise Exception("Access token not returned. Check refresh token / client credentials.")

    return data["access_token"]