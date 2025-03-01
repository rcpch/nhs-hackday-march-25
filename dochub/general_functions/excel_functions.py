import os
import pandas as pd
from django.conf import settings

def get_unique_specialties():
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

    # print a list of all unqiue specialties
    print(df['Post Specialty'].unique())
    return df

