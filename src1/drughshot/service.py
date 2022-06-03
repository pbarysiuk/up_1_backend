import json
import requests

DRUGSHOT_URL = 'https://maayanlab.cloud/drugshot/api/{}'


def search(payload: dict) -> dict:
    response = requests.post(DRUGSHOT_URL.format("search"), json=payload)
    return json.loads(response.text)


def associate(payload: dict) -> dict:
    response = requests.post(DRUGSHOT_URL.format("associate"), json=payload)
    return json.loads(response.text)
