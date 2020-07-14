import sqlite3
import sys
import census_api as c
import database

arguments = [x.upper() for x in sys.argv[1:]]
years = range(2011, 2019) #range does not include 2019
states = database.get_states()

tables = [,'comparison_prifile.csv','data_profiles.csv','detailed_tables.csv','get_variables.py','selected_population_profiles.csv','subject_tables.csv']


def process_arg(arg):
    data_set = tables[arg[0]]
    print(data_set)
    for year in years:
        arg = arg.upper()
        for state in states:
            stateid = f'{state[0]:02}'
            try:
                region = f'county:*&in=state:{stateid}'
                result = data_set(get=f'NAME,{arg}', year=year, region=region)
                print(result)
            except Exception as e:
                print(e)
                continue
            for r in result[1:]:
                countyid = r[2]
                countyname = ''.join([x for x in r[0].split(',')[0] if x.isalpha()])
                statename = ''.join([x for x in r[0].split(',')[1] if x.isalpha()])
                table_name = f'{arg}_{countyname}'
                database.create_dataset(table_name, stateid) #takes in result information 
                data_input = [year, 0 if r[1] == None else r[1], countyid, int(stateid)]
                print(data_input)
                database.populate_dataset(table_name, data_input)
            

if __name__ == '__main__':
    for arg in arguments:
        process_arg(arg)
    '''
        #get the argument and call appropriate api
        if arg[:3] == 'S02':
            data_set = c.population_profiles
        elif arg[:3] == 'S01':
            data_set = c.subject_tables
        else:
            data_set = tables[arg[0]]
        #start to loop through each year
        for year in years:
            #loop through each state in states
            for state in states:
                stateid = f'{state[0]:02}'
                statename = state[1]
                #loop through each county in each state
                counties = database.get_counties(statename.replace(' ',''))
                try:
                    for c in counties[1:]:
                        countyname = c[3]
                        countyname = countyname.replace('-','')
                        county = f'{c[2]:03}'
                        #dataset returns a JSON object
                        region = f'county:{county}&in=state:{stateid}'
                        result = data_set(get=arg, year=year, region=region)
                        #call function from database to make new table and populate new table
                        if result[1][0] == None:
                            result[1][0] = 0
                        table_name = f'{arg}_{countyname}'
                        database.create_dataset(table_name, stateid) #takes in result information 
                        data_input = [year, result[1][0], int(county), int(stateid)]
                        print(data_input)
                        database.populate_dataset(table_name, data_input)
                except Exception as e:
                    print(e)
