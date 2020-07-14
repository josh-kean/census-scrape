import sqlite3
import time
import urllib.request as url
import sys
import json
from sql_connect import sql_connect

api_key = 'a15f9f0e3cc9f5d60e635e55a58a73104ff52fe3'

#three databases for now; states and their state id
#counties for each state
#group and all group variables per county


#returns a list of all tables
@sql_connect
def get_tables(curs):
    tables = curs.execute('select name from sqlite_master where type = \'table\'')
    return [table[0] for table in tables.fetchall()]

#drops the specific table
@sql_connect
def drop_table(curs, table):
    sqlTxn = f'drop table if exists {table}'
    curs.execute(sqlTxn)

#clear every table in the census-information database
def clear_database():
    print('activate')
    tables = get_tables()
    for table in tables:
        drop_table(table)

#returns all the states from the states table
@sql_connect
def get_states(curs):
    states = curs.execute('select * from states')
    return states.fetchall()

#returns all the counties of a given state
@sql_connect
def get_counties(curs,state):
    counties = curs.execute(f'select * from {state}')
    return counties.fetchall()

#creates a table with specific census values
@sql_connect
def create_data_table(curs,table_name, stateid, countyid, data):
    #data is a 2d array where x[0] is dataset name and x[1] is datatype
    #make a string of all data types and floats
    dat_columns = ','.join([f' {x[0]} decimal' for x in data]
    #tablename should be group_county_state
    sqlTxn = f'create table if not exists {table_name}(year int, {dat_columns}, stateid int, foreign key (stateid) references states(stateid))'
    curs.execute(sqlTxn)

#takes a specific uscensus variable and populates a table with it
@sql_connect
def populate_dataset(curs,table_name, data):
    curs.execute(f'insert into {table_name} values(?,?,?,?)', (int(data[0]), data[1],int(data[2]), int(data[3])))

#inserts into the 'states' table all the states and their uscensus codes
@sql_connect
def create_state_database(curs,stateid, statename):
    curs.execute('insert into states values(?, ?)', (int(stateid), statename))

#creates a database of all the counties within a given state
@sql_connect
def create_county_database(curs,statename):
    sqltxn = f'create table if not exists {statename}(stateid int, statename char, countyid int primary key, countyname text, foreign key (stateid) references states(stateid))'
    curs.execute(sqltxn)

#creates a single database with each state and stateid in it. does not include several states if not included in census informatio
@sql_connect
def create_states(curs):
    curs.execute('create table if not exists states(stateid int primary key, statename char(30))')
    for x in range(1, 55):
        if x < 10:
            x = '0'+str(x)
        try:
            result = url.urlopen(f'https://api.census.gov/data/2018/acs/acs1/cprofile?get=NAME&for=state:{x}')
            result = json.loads(result.read())
            [statename, stateid] = result[1]
            create_state_database(stateid, statename.replace(' ',''))
            time.sleep(.1)
        except:
            print(f'{x} state failed')


#gets each county within a state and creates a row for each county in a database per state
@sql_connect
def populate_county(curs,stateid):
    result = url.urlopen(f'https://api.census.gov/data/2018/acs/acs1/cprofile?get=NAME&for=county:*&in=state:{stateid}')
    result = json.loads(result.read())
    statename = result[1][0].split(',')[1].replace(' ','')
    time.sleep(.5)
    values = [[stateid, statename, x[2], x[0].split(',')[0].replace(' ','').replace('-','')] for x in result]
    curs.executemany(f'insert into {statename} values (?, ?, ?, ?)', values)

#iterates through all the state tables and does the following
#1. creates a database for each state which keeps track of each county within that state
#2. populates each state table with all the counties found within that state
def create_counties(curs):
    states = get_states()
    for state in states:
        create_county_database(state[1].replace(' ',''))
        populate_county(f'{state[0]:02}')

if __name__ == '__main__':
    relevant_functions = {
            'clear_db': clear_database,
            'states': create_states,
            }

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if relevant_functions.get(arg):
                relevant_functions[arg]()
