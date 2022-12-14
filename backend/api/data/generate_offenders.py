payload = {
    "addresses": [
        {
            "line": ""
        }
    ],
    "names": [
        {
            "first_name": "",
            "last_name": "",
            "middle": ""
        }
    ],
    "dob": {
        "year": 1980,
        "month": 1,
        "day": 1
    },
    "demographic": {
        "height": "4' 3\"",
        "race": "",
        "sex": "MALE",
        "weight": "145 Lbs."
    },
    "cases": [
        {
            "case_number": "",
            "charges": [
                {
                    "description": "Abuse of Minor e",
                    "offense_date": "2012-3-15"
                }
            ]
        }
    ]
}


import requests
import random
import uuid
import time

from payload import first_names, last_names, races, address_lines
# NOTE source venv/bin/activate
# NOTE cd backend/api/data/ && python generate_offenders.py
# NOTE paste your token
token = "<paste your token here>"

base_url = f"http://localhost:5000/api/v1/"
endpoint = f"offenders/"
url = f"{base_url}{endpoint}"
headers = {"Authorization": f"Bearer {token}"}


idx = 0
for fn, ln, addr in zip(first_names, last_names, address_lines):
    address_line = addr
    first_name = fn
    last_name = ln
    case_number = uuid.uuid4().hex
    race = random.choice(races)
    year = random.randint(1970, 2000)
    month = random.randint(3,12)
    day = random.randint(1,30)

    payload["addresses"][0]["line"] = address_line
    payload["names"][0]["first_name"] = first_name
    payload["names"][0]["last_name"] = last_name
    payload["dob"]["year"] = year
    payload["dob"]["month"] = month
    payload["dob"]["day"] = day
    payload["demographic"]["race"] = race
    payload["cases"][0]["case_number"] = case_number

    try:
        requests.post(url, json=payload, headers=headers)
        time.sleep(0.001)
    except:
        print("ERROR: ")
        print(payload)
        print()


