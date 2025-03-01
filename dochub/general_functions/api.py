import requests
from django.conf import settings

def fetch_local_health_boards():
    request_url = f"{settings.ORGANISATIONS_BASE_URL}/local_health_boards"

    response = requests.get(request_url, timeout=10)
    response.raise_for_status()

    return response.json()


def fetch_trusts():
    request_url = f"{settings.ORGANISATIONS_BASE_URL}/trusts"

    response = requests.get(request_url, timeout=10)
    response.raise_for_status()

    return response.json()


def fetch_organisations():
    request_url = f"{settings.ORGANISATIONS_BASE_URL}/organisations"

    response = requests.get(request_url, timeout=10)
    response.raise_for_status()

    return response.json()