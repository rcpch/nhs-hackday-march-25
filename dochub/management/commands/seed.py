import requests
from django.apps import apps
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

ORGANISATIONS_BASE_URL = "https://rcpch-nhs-organisations.azurewebsites.net/"

def fetch_local_health_boards():
    request_url = f"{ORGANISATIONS_BASE_URL}/local_health_boards"

    response = requests.get(request_url, timeout=10)
    response.raise_for_status()

    return response.json()



def add_local_health_boards():
    Parent = apps.get_model("dochub", "Parent")

    request_url = f"{ORGANISATIONS_BASE_URL}/local_health_boards"

    response = requests.get(request_url, timeout=10)
    response.raise_for_status()

    lhb_data = response.json()
    
    for lhb in lhb_data:
        Parent.objects.create(
            ods_code = lhb["ods_code"],
            name = lhb["name"],
            welsh_name = lhb["welsh_name"],
            location_bng = Point(lhb["bng_e"], lhb["bng_n"])
        )

def add_trusts():
    Parent = apps.get_model("dochub", "Parent")

    request_url = f"{ORGANISATIONS_BASE_URL}/trusts"

    response = requests.get(request_url, timeout=10)
    response.raise_for_status()

    data = response.json()
    
    for trust in data:
        Parent.objects.create(
            ods_code = trust["ods_code"],
            name = trust["name"]
        )


class Command(BaseCommand):
    help = "seed database with local health boards and trusts and their child organisations"

    def handle(self, *args, **options):
        add_local_health_boards()
        # add_trusts()

        