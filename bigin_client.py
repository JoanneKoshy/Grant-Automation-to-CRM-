import requests
import re
import json
from datetime import datetime
from bigin_auth import get_access_token

def clean_amount(amount_str):
    cleaned = re.sub(r'[^\d.]', '', str(amount_str))
    return float(cleaned) if cleaned else 0.0

def clean_date(date_str):
    if not date_str or "unable" in date_str.lower() or "n/a" in date_str.lower():
        return None
    try:
        date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
        parsed = datetime.strptime(date_str.strip(), "%B %d, %Y")
        return parsed.strftime("%Y-%m-%d")
    except:
        return None

def push_to_bigin(grant_data: dict):

    access_token = get_access_token()

    url = "https://www.zohoapis.in/bigin/v2/Pipelines"

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "data": [
            {
                "Deal_Name": grant_data["oppurtunity_name"],
                "Layout": {"id": "645408000000471242"},
                "Sub_Pipeline": "Funding Applications Standard",
                "Stage": "Applications Identified",
                "Website": grant_data["website"],
                "Amount": clean_amount(grant_data["amount"]),
                "Type_of_Opportunity": grant_data["type_of_oppurtunity"],
                "First_Draft_date": clean_date(grant_data["first_draft_date"]),
                "Submission_Date": clean_date(grant_data["submission_deadline"]),
                "Description": grant_data["description"]
            }
        ]
    }

    print("PAYLOAD BEING SENT:", json.dumps(payload, indent=2))

    response = requests.post(url, headers=headers, json=payload)

    print("Status:", response.status_code)
    print("Response:", response.text)

    return response.json()