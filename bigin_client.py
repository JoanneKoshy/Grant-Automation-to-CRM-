import requests
from bigin_auth import get_access_token

MODULE_NAME = "Deals"

def push_to_bigin(grant_data: dict):

    access_token = get_access_token()

    url = f"https://www.zohoapis.in/bigin/v2/{MODULE_NAME}"

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "data": [
            {
                "Deal_Name": grant_data["oppurtunity_name"],
                "Pipeline": "Funding Applications",
                "Stage": "Applications Identified",
                "Website": grant_data["website"],
                "Amount": grant_data["amount"],
                "Type_of_Opportunity": grant_data["type_of_oppurtunity"],
                "First_Draft_date": grant_data["first_draft_date"],
                "Submission_Date": grant_data["submission_deadline"],
                "Description": grant_data["description"]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    print("Status:", response.status_code)
    print("Response:", response.text)

    return response.json()