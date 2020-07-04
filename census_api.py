import time
import urllib.request as url
import json

api_key = 'a15f9f0e3cc9f5d60e635e55a58a73104ff52fe3'

def detailed_tables(get='B01001_001E', year='2018', region='state:02'):
    result = url.urlopen(f'https://api.census.gov/data/{year}/acs/acs1?get={get}&for={region}&key={api_key}')
    return json.loads(result.read())

def subject_tables(get, year, region):
    result = url.urlopen(f'https://api.census.gov/data/{year}/acs/acs1/subject?get={get}&for={region}&key={api_key}')
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

def call_api(data_set, get, start_state=1, end_state=10, start_year=2017, end_year=2018, national=False):
    result = []
    for state in range(start_state, end_state+1):
        if state < 10:
            state = '0'+str(state)
        for year in range(start_year, end_year+1):
            time.sleep(1)
            try:
                if national:
                    new_json = data_set(get=get, year=end_year, region=f'us:1')
                    print(new_json)
                    break
                else:
                    new_json = data_set(get=get, year=year, region=f'county:*&in=state:{state}')
                for row in new_json:
                    print(row)
            except Exception as e:
                print(e)

#call_api(data_set=subject_tables, end_state=20, get='NAME&S0501_C01_135E')
call_api(data_set=data_profiles, start_state=10, end_state=20, get='NAME&DP04_0003PE')



'''
for x in range(1,51):
    time.sleep(3)
    if x < 10:
        x = '0'+str(x)
    try:
        new_json = detailed_tables(get='NAME&B01001A_009E',region=f'county:*&in=state:{x}')
        print(new_json)
    except Exception as e:
        print(e)
        '''
