import json
import urllib.request as url
import csv

detail_link = 'https://api.census.gov/data/2018/acs/acs1/variables.json'
subject_link = 'https://api.census.gov/data/2018/acs/acs1/subject/variables.json'
data_profiles = 'https://api.census.gov/data/2018/acs/acs1/profile/variables.json'
comparison_profile = 'https://api.census.gov/data/2018/acs/acs1/cprofile/variables.json'
population_profiles = 'https://api.census.gov/data/2018/acs/acs1/cprofile/variables.json'

links = [detail_link, subject_link, data_profiles, comparison_profile, population_profiles]

table_names = {
        0: 'detailed_tables',
        1: 'subject_tables',
        2: 'data_profiles',
        3: 'comparison_prifile',
        4: 'selected_population_profiles'
        }

def open_link(link):
    result = url.urlopen(link)
    return json.loads(result.read())

def save_info(i, data):
    w = csv.writer(open(f'{table_names[i]}.csv', 'a', newline=''))
    w.writerow(data)

if __name__ == '__main__':
    for i, link in enumerate(links):
        variables = open_link(link)['variables']
        keys = list(variables.keys())[4:]
        for x in keys:
            if variables[x].get('predicateType'):
                #data = [x, variables[x]['predicateType'], variables[x]['label']]
                save_info(i, data)
