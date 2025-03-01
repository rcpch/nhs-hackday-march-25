from django.apps import apps
from ....general_functions.api import fetch_integrated_care_boards, fetch_local_health_boards, fetch_nhs_england_regions, fetch_trusts, fetch_organisations

def seed_icbs():
    # the orginally seeded boundaries do not include ods_code
    IntegratedCareBoard = apps.get_model('dochub', 'IntegratedCareBoard')

    icbs = fetch_integrated_care_boards()

    for icb in icbs:
        IntegratedCareBoard.objects.update_or_create(
            boundary_identifier=icb['boundary_identifier'],
            defaults={
                'ods_code':icb['ods_code'],
                'name': icb['name'],
                'bng_e': icb['bng_e'],
                'bng_n': icb['bng_n'],
                'long': icb['long'],
                'lat': icb['lat'],
            }
        )
    print(f"Integrated Care Boards seeded. {len(icbs)} records added.")

def seed_lhbs():
    # the orginally seeded boundaries do not include ods_code
    LocalHealthBoard = apps.get_model('dochub', 'LocalHealthBoard')

    lhbs = fetch_local_health_boards()

    for lhb in lhbs:
        LocalHealthBoard.objects.update_or_create(
            boundary_identifier = lhb['boundary_identifier'],
            defaults={
                'ods_code':lhb['ods_code'],
                'name': lhb['name'],
                'welsh_name': lhb['welsh_name'],
                'bng_e': lhb['bng_e'],
                'bng_n': lhb['bng_n'],
                'long': lhb['long'],
                'lat': lhb['lat'],
            }
        )
    print(f"Local Health Boards seeded. {len(lhbs)} records added.")

def seed_nhsers():
    # the orginally seeded boundaries do not include region_code
    NhsEnglandRegion = apps.get_model('dochub', 'NhsEnglandRegion')

    nhsers = fetch_nhs_england_regions()

    for nhser in nhsers:
        NhsEnglandRegion.objects.update_or_create(
            boundary_identifier = nhser['boundary_identifier'],
            defaults={
                'region_code':nhser['region_code'],
                'name': nhser['name'],
                'bng_e': nhser['bng_e'],
                'bng_n': nhser['bng_n'],
                'long': nhser['long'],
                'lat': nhser['lat'],
            }
        )
    print(f"NHS England Regions seeded. {len(nhsers)} records added.")

def seed_trusts():
    Trust = apps.get_model('dochub', 'Trust')

    trusts = fetch_trusts()
    
    for trust in trusts:
        Trust.objects.update_or_create(
            ods_code=trust['ods_code'],
            defaults={
                "name": trust['name'],
                "address_line_1": trust['address_line_1'],
                "address_line_2": trust['address_line_2'],
                "town": trust['town'],
                "postcode": trust['postcode'],
                "country": trust['country'],
                "telephone": trust['telephone'],
                "website": trust['website']
            }
        )
    print(f"Trusts seeded. {len(trusts)} records added.")

def seed_organisations():
    Organisation = apps.get_model('dochub', 'Organisation')
    Trust = apps.get_model('dochub', 'Trust')
    LocalHealthBoard = apps.get_model('dochub', 'LocalHealthBoard')
    IntegratedCareBoard = apps.get_model('dochub', 'IntegratedCareBoard')
    NHSEnglandRegion = apps.get_model('dochub', 'NHSEnglandRegion')
    Country = apps.get_model('dochub', 'Country')

    organisations = fetch_organisations()

    for organisation in organisations:
        model_organisation, created = Organisation.objects.update_or_create(
            ods_code=organisation['ods_code'],
            defaults={
                "name": organisation['name'],
                "website": organisation['website'],
                "address1": organisation['address1'],
                "address2": organisation['address2'],
                "address3": organisation['address3'],
                "telephone": organisation['telephone'],
                "city": organisation['city'],
                "county": organisation['county'],
                "latitude": organisation['latitude'],
                "longitude": organisation['longitude'],
                "postcode": organisation['postcode'],
            }
        )

        # Set the parent
        if organisation['local_health_board'] is not None and organisation['trust'] is None:
            model_organisation.local_health_board = LocalHealthBoard.objects.get(ods_code=organisation['local_health_board']['ods_code'])
        elif organisation['trust']  is not None and organisation['local_health_board'] is None:
            model_organisation.trust = Trust.objects.get(ods_code=organisation['trust']['ods_code'])
            # exclude Jersey and Guernsey
            if organisation['country']['boundary_identifier'] != "E92000003":
                model_organisation.integrated_care_board  = IntegratedCareBoard.objects.get(ods_code=organisation['integrated_care_board']['ods_code'])
                model_organisation.nhs_england_region = NHSEnglandRegion.objects.get(region_code=organisation['nhs_england_region']['region_code'])
                # set the country
                model_organisation.country = Country.objects.get(boundary_identifier=organisation['country']['boundary_identifier'])
        
        model_organisation.save()
    print(f"Organisations seeded. {len(organisations)} records added.")