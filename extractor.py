import os
import json
import re
from datetime import datetime, timedelta
from groq import Groq
from schemas import GrantDetails


def extract_grant_details(raw_text: str, url: str):

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
You are an expert grant analyst.

Extract the following details from the grant information below.

Type of opportunity must be one of:
applications, awards, events, other opportunities, accelerator, pilot, grants, investments.

Return ONLY valid JSON in this exact format:

{{
  "oppurtunity_name": "",
  "type_of_oppurtunity": "",
  "amount": "",
  "submission_deadline": "",
  "description": ""
}}

Grant Information:
{raw_text[:8000]}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    response_text = completion.choices[0].message.content.strip()

    # Extract JSON safely
    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if not match:
        raise ValueError("No valid JSON found in model response.")

    data = json.loads(match.group())

    # ---- Calculate first_draft_date (1 week before deadline) ----
    submission_deadline = data.get("submission_deadline", "")
    first_draft_date = ""

    date_formats = [
        "%d %B %Y",     # 23 March 2026
        "%B %d, %Y",    # March 23, 2026
        "%d %b %Y",     # 23 Mar 2026
        "%b %d, %Y"     # Mar 23, 2026
    ]

    parsed_date = None

    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(submission_deadline.strip(), fmt)
            break
        except:
            continue

    if parsed_date:
        first_draft = parsed_date - timedelta(days=7)
        first_draft_date = first_draft.strftime("%B %d, %Y")
    else:
        first_draft_date = "Unable to auto-calculate"

    # Final structured data
    final_data = {
        "oppurtunity_name": data.get("oppurtunity_name", ""),
        "website": url,
        "type_of_oppurtunity": data.get("type_of_oppurtunity", ""),
        "amount": data.get("amount", ""),
        "submission_deadline": submission_deadline,
        "first_draft_date": first_draft_date,
        "description": data.get("description", "")
    }

    return GrantDetails(**final_data)