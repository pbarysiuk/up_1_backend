import json
import requests


def search(payload: dict) -> dict:
    DRUGSHOT_URL = 'https://maayanlab.cloud/drugshot/api/search'
    response = requests.post(DRUGSHOT_URL, json=payload)
    return json.loads(response.text)
