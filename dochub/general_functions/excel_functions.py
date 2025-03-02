import os
import pandas as pd
from django.conf import settings
from django.apps import apps

from ..constants import INDICATOR_CHOICES, BENCHMARK_CHOICES, POST_SPECIALITY_CHOICES

def import_gmc_data():
    """
    Read an excel file and return a pandas dataframe.
    
    :param
    file_path: str, path to the excel file

    :return
    df: pandas dataframe
    """
    # get path of file in root of application
    file_path = os.path.join(settings.BASE_DIR,'dochub', 'data', 'nts-ltd-postspecbysite-2024_xlsx-107341611.xlsx')
    df = pd.read_excel(file_path)

    # import the data into django model
    GMC = apps.get_model('dochub', 'GMC')
    Organisation = apps.get_model('dochub', 'Organisation')

    # column names
    headers = ['#Geo_LETB_Deanery', 'Post_Specialty', 'Trust_Board', 'Site', 'Indicator', 'Year', 'Outcome', 'Response_Rate', 'Mean', 'CI_Lower', 'CI_Upper', 'N_Range', 'Benchmark_Name', 'National_Mean', 'National_Min', 'National_Q1', 'National_Median', 'National_Q3', 'National_Max', 'National_CI_Lower', 'National_CI_Upper', 'National_N']

    # The Site column unfortunately has the ODS code appended to the name of the Site heading after a -

    # iterate through the dataframe and save each row as an instance of the GMC model
    # note the specialty and the indicator map to the choices in the GMC model

    for index, row in df.iterrows():
        deanery_name, post_specialty, trust_board, site, indicator, year, outcome, response_rate, mean, ci_lower, ci_upper, n_range, benchmark_name, national_mean, national_min, national_Q1, national_median, national_Q3, national_max, national_ci_lower, national_ci_upper, national_n = row

        # get the specialty
        post_specialty = post_specialty.strip()
        post_specialty = [choice[0] for choice in POST_SPECIALITY_CHOICES if choice[1] == post_specialty][0]
        # get the key of the indicator
        indicator = [choice[0] for choice in INDICATOR_CHOICES if choice[1] == indicator]
        indicator = indicator[0] if indicator else None
        
        # get the key of the benchmark
        benchmark_name = benchmark_name.strip()
        benchmark_name = [choice[0] for choice in BENCHMARK_CHOICES if choice[1] == benchmark_name.strip()][0]

        site_ods_code=site.split('-')[1].strip()
        try:
            organisation = Organisation.objects.get(ods_code=site_ods_code)
        except Organisation.DoesNotExist:
            print(f"Organisation with ODS code {site_ods_code} does not exist")
            continue

        # save the instance
        GMC.objects.create(
            deanery_name=deanery_name,
            post_specialty=post_specialty,
            indicator=indicator,
            year=year,
            outcome=outcome,
            response_rate=response_rate,
            mean=mean,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            n_range=n_range,
            benchmark_name=benchmark_name,
            national_mean=national_mean,
            national_min=national_min,
            national_Q1=national_Q1,
            national_median=national_median,
            national_Q3=national_Q3,
            national_max=national_max,
            national_ci_lower=national_ci_lower,
            national_ci_upper=national_ci_upper,
            national_n=national_n,
            organisation=organisation
        )
    
    return df

