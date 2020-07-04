import sys
import census_api as c
import database

arguments = [x.upper() for x in sys.argv[1:]]
years = range(2011, 2019) #range does not include 2019
states = database.get_states()

tables = {
        'B': c.detailed_tables,
        'S': c.subject_tables,
        'D': c.data_profiles,
        'C': c.comparison_profiles,
        }

[print(x) for x in states]

if __name__ == '__main__':
    for arg in arguments:
        #get the argument and call appropriate api
        data_set = tables[arg[0]]
        #start to loop through each year
        for year in years:
            #loop through each state in states
            for state in states:
                #loop through each county in each state
                counties = database.get_counties()
                for county, countyname in counties:
                    #dataset returns a JSON object
                    result = data_set(get=arg, year=year, region=f'county:{county}&in=state:{state}')
                    #call function from database to make new table and populate new table
                    table_name = f'{arg}_{countyname}'
                    c.create_dataset(table_name, arg) #takes in result information 
                    c.populate_dataset(table_name, result[1])
