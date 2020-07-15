import pytest
import census_api as c
import main as m
import table_variables.get_variables as gb
import urllib.request as url
import json

api_key = 'a15f9f0e3cc9f5d60e635e55a58a73104ff52fe3'

def open_page(urlCall):
    result = url.urlopen(urlCall)
    data = json.loads(result.read())
    return data

def test_detailed_tables_call():
    urlCall = f'https://api.census.gov/data/2018/acs/acs1?get=B01001_001E&for=state:02&key={api_key}'
    assert open_page(urlCall) == c.detailed_tables()

def test_subject_tables_call():
    urlCall = f'https://api.census.gov/data/2018/acs/acs1/subject?get=S2701_C04_052E&for=state:02&key={api_key}'
    assert open_page(urlCall) == c.subject_tables()

def test_data_profiles_call():
    urlCall = f'https://api.census.gov/data/2018/acs/acs1/profile?get=DP02_0005E&for=state:02&key={api_key}'
    assert open_page(urlCall) == c.data_profiles()

def test_comparison_profiles_call():
    urlCall = f'https://api.census.gov/data/2018/acs/acs1/cprofile?get=CP02_2014_007E&for=state:02&key={api_key}'
    assert open_page(urlCall) == c.comparison_profiles()

def test_population_profiles_call():
    urlCall = f'https://api.census.gov/data/2018/acs/acs1/spp?get=S0201_007E&for=state:02&key={api_key}'
    assert open_page(urlCall) == c.population_profiles()


