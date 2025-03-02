from django.apps import apps
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from .seed_functions import seed_trusts, seed_organisations, seed_icbs, seed_nhsers, seed_lhbs
from ...general_functions import import_gmc_data



class Command(BaseCommand):
    help = "seed database with local health boards and trusts and their child organisations"

    def add_arguments(self, parser):
        parser.add_argument(
            "-m",
            "--mode",
            type=str,
            help="Mode - seed options to include: trusts, organisations",
        )

    def handle(self, *args, **options):
        if options["mode"] == 'local_health_boards':
            seed_lhbs()

        if options["mode"] == 'nhs_england_regions':
            seed_nhsers()

        if options["mode"] == 'icbs':
            seed_icbs()

        if options["mode"] == "trusts":
            seed_trusts()
        
        if options["mode"] == "organisations":
            seed_organisations()

        if options["mode"] == "gmc":
            # seed the GMC data
            import_gmc_data()

        if options["mode"] == "all":
            # update all the boundaries with correct codes
            seed_lhbs()
            seed_nhsers()
            seed_icbs()
            # add all the trusts
            seed_trusts()
            # add all the organisations and relationships with previous
            seed_organisations()
