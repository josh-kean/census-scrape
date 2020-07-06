import sqlite3
import sys
import census_api as c
import database

arguments = [x.upper() for x in sys.argv[1:]]
years = range(2011, 2019) #range does not include 2019
states = database.get_states()

tables = {
        'B': c.detailed_tables,
        'D': c.data_profiles,
        'C': c.comparison_profiles,
        }

if __name__ == '__main__':
    for arg in arguments:
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
                        table_name = f'{arg.replace("_","")}{countyname}'
                        print('this works: ',table_name, result[1])
                        database.create_dataset(table_name) #takes in result information 
                        print('made table')
                        #print('after create_dataset, arg: ',arg)
                        #database.populate_dataset(table_name, )
                except Exception as e:
                    print(e)
