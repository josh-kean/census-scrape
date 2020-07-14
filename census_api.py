import time
import urllib.request as url
import json

api_key = 'a15f9f0e3cc9f5d60e635e55a58a73104ff52fe3'

def detailed_tables(get='B01001_001E', year='2018', region='state:02'):
    urlCall = f'https://api.census.gov/data/{year}/acs/acs1?get={get}&for={region}&key={api_key}'
    result = url.urlopen(urlCall)
    data = json.loads(result.read())
    return data

def subject_tables(get, year, region):
    urlCall = f'https://api.census.gov/data/{year}/acs/acs1/subject?get={get}&for={region}&key={api_key}'
    result = url.urlopen(urlCall)
    return json.loads(result.read())

def data_profiles(get, year, region):
    result = url.urlopen(f'https://api.census.gov/data/{year}/acs/acs1/profile?get={get}&for={region}&key={api_key}')
    return json.loads(result.read())

def comparison_profiles(get, year, region):
    result = url.urlopen(f'https://api.census.gov/data/{year}/acs/acs1/cprofile?get={get}&for={region}&key={api_key}')
    return json.loads(result.read())

def population_profiles(get, year, region):
    result = url.urlopen(f'https://api.census.gov/data/{year}/acs/acs1/spp?get={get}&for={region}&key={api_key}')
    return json.loads(result.read())

