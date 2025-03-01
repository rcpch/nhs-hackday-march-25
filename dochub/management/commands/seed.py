from django.apps import apps
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from dochub.general_functions.api import fetch_local_health_boards, fetch_trusts, fetch_organisations




class Command(BaseCommand):
    help = "seed database with local health boards and trusts and their child organisations"

    def handle(self, *args, **options):
        Parent = apps.get_model("dochub", "Parent")
        Organisation = apps.get_model("dochub", "Organisation")

        local_health_boards = fetch_local_health_boards()
        trusts = fetch_trusts()
        organisations = fetch_organisations()

        for lhb in local_health_boards:
            Parent.objects.create(
                ods_code = lhb["ods_code"],
                name = lhb["name"],
                welsh_name = lhb["welsh_name"],
                # TODO SIMON!!! Which field should we use here?
                # location_bng = Point(lhb["bng_e"], lhb["bng_n"])
            )

        for trust in trusts:
            # seems like there's some health boards in the trusts data
            if not Parent.objects.filter(ods_code=trust["ods_code"]).exists():
                Parent.objects.create(
                    ods_code = trust["ods_code"],
                    name = trust["name"]
                )
        
        for organisation in organisations:
            if organisation["local_health_board"]:
                parent_ods_code = organisation["local_health_board"]["ods_code"]
            elif organisation["trust"]:
                parent_ods_code = organisation["trust"]["ods_code"]
            
            print(f"!! {parent_ods_code}")
            parent = Parent.objects.get(ods_code=parent_ods_code)

            Organisation.objects.create(
                ods_code = organisation["ods_code"],
                name = organisation["name"],
                # TODO SIMON!!! Which field should we use here?
                # location_bng = Point(organisation["bng_e"], organisation["bng_n"]),
                parent = parent
            )
