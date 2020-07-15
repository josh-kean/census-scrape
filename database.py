import sqlite3
import time
import urllib.request as url
import sys
import json
from sql_connect import sql_connect

api_key = 'a15f9f0e3cc9f5d60e635e55a58a73104ff52fe3'
states = []

#three databases for now; states and their state id
#counties for each state
#group and all group variables per county


#returns a list of all tables
def get_tables():
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    tables = curs.execute('select name from sqlite_master where type = \'table\'')
    tables = [table[0] for table in tables.fetchall()]
    conn.commit()
    return tables

#drops the specific table
@sql_connect
def drop_table(curs, table):
    sqlTxn = f'drop table if exists {table}'
    curs.execute(sqlTxn)

#clear every table in the census-information database
def clear_database():
    tables = get_tables()
    for table in tables:
        drop_table(table)

#returns all the states from the states table
def get_states():
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    states = curs.execute('select * from states')
    conn.commit()
    return states.fetchall()

#returns all the counties of a given state
def get_counties(state):
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    sqlTxn = f'select * from {state}'
    counties = curs.execute(sqlTxn)
    conn.commit()
    return counties.fetchall()

#creates a table with specific census values
@sql_connect
def create_data_table(curs, table_name, stateid, countyid, data):
    #data is a 2d array where x[0] is dataset name and x[1] is datatype
    #make a string of all data types and floats
    #tablename should be group_county_state
    sqlTxn = f'create table if not exists {table_name}(year int, {data}, stateid int, countyid int, foreign key (stateid) references states(stateid))'
    curs.execute(sqlTxn)

#takes a specific uscensus variable and populates a table with it
@sql_connect
def populate_dataset(curs,table_name, stateid, countyid, data, year):
    dat_columns = ','.join([f' {x[0]}' for x in data])
    sqlTxn = f'insert into {table_name} values(?, {"?,"*len(data)} ?, ?)'
    curs.execute(sqlTxn, (year, *[x[1] for x in data], stateid, countyid))

#inserts into the 'states' table all the states and their uscensus codes
@sql_connect
def create_state_database(curs, stateid, statename):
    states = curs.execute('select * from states')
    if statename not in [x[1] for x in states.fetchall()]:
        curs.execute('insert into states values(?, ?)', (int(stateid), statename))

#creates a database of all the counties within a given state
@sql_connect
def create_county_database(curs,statename):
    sqltxn = f'create table if not exists {statename}(stateid int, statename char, countyid int primary key, countyname text, foreign key (stateid) references states(stateid))'
    curs.execute(sqltxn)


#gets each county within a state and creates a row for each county in a database per state
@sql_connect
def populate_county(curs,stateid):
    result = url.urlopen(f'https://api.census.gov/data/2018/acs/acs1/cprofile?get=NAME&for=county:*&in=state:{stateid}')
    result = json.loads(result.read())
    statename = result[1][0].split(',')[1].replace(' ','')
    counties = curs.execute(f'select * from {statename}')
    counties = [x[2] for x in counties]
    values = [[stateid, statename, x[2], x[0].split(',')[0].replace(' ','').replace('-','')] for x in result if x[2] not in counties]
    if len(values) > 0:
        curs.executemany(f'insert into {statename} values (?, ?, ?, ?)', values)

#creates the table that contains all us states
@sql_connect
def create_states_table(curs):
    curs.execute('create table if not exists states(stateid int primary key, statename char(30))')

def populate_states_table():
    for x in range(1, 55):
        if x < 10:
            x = '0'+str(x)
        try:
            result = url.urlopen(f'https://api.census.gov/data/2018/acs/acs1/cprofile?get=NAME&for=state:{x}')
            result = json.loads(result.read())
            [statename, stateid] = result[1]
            create_state_database(stateid, statename.replace(' ',''))
        except Exception as e:
            pass

#iterates through all the state tables and does the following
#1. creates a database for each state which keeps track of each county within that state
#2. populates each state table with all the counties found within that state
def create_counties():
    states = get_states()
    for state in states:
        create_county_database(state[1].replace(' ',''))
        populate_county(f'{state[0]:02}')


if __name__ == '__main__':
    #creates a database of states
    create_states_table()
    populate_states_table()
    #create a table for each state and fill it with counties
    create_counties()
