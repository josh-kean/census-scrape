import sqlite3
import time
import urllib.request as url
import json

api_key = 'a15f9f0e3cc9f5d60e635e55a58a73104ff52fe3'

#three databases for now; states and their state id
#counties for each state
#vacancies per county per year

def get_tables():
    conn = sqlite3.connect('census-information')
    curs = conn.cursor()
    tables = curs.execute('select name from sqlite_master where type = \'table\'')
    return [table[0] for table in tables.fetchall()]

def get_states():
    conn = sqlite3.connect('census-information')
    curs = conn.cursor()
    states = curs.execute('select * from states')
    return states

def get_counties(state):
    conn = sqlite3.connect('census-information')
    curs = conn.cursor()
    counties = curs.execute(f'select * from {state}')
    return counties

def create_dataset(table_name, data):
    conn = sqlite3.connect('census-information')
    curs = conn.cursor()
    curs.execute('create table if not exists {table_name} (year char primary key, data char)')
    conn.commit()

def populate_dataset(table_name, data):
    conn = sqlite3.connect('census-information')
    curs = conn.cursor()
    curs.executemany('insert into {table_name} (?,?)' data)
    conn.commit()

def create_state_database(stateid, statename):
    conn = sqlite3.connect('census-information')
    curs = conn.cursor()
    curs.execute('insert into states values(?, ?)', (int(stateid), statename))
    conn.commit()

def create_county_database(statename):
    conn = sqlite3.connect('census-information')
    curs = conn.cursor()
    sqltxn = f'create table if not exists {statename}(stateid int, statename char, countyid int primary key, countyname text, foreign key (stateid) references states(stateid))'
    curs.execute(sqltxn)
    #conn.commit()

def create_states():
    conn = sqlite3.connect('census-information')
    curs = conn.cursor()
    curs.execute('create table if not exists states(stateid int primary key, statename char(30))')
    conn.commit()
    for x in range(1, 55):
        if x < 10:
            x = '0'+str(x)
        try:
            result = url.urlopen(f'https://api.census.gov/data/2018/acs/acs1/cprofile?get=NAME&for=state:{x}')
            result = json.loads(result.read())
            [statename, stateid] = result[1]
            create_state_database(stateid, statename)
            time.sleep(.5)
        except:
            print(f'{x} state failed')


def populate_county(stateid):
    result = url.urlopen(f'https://api.census.gov/data/2018/acs/acs1/cprofile?get=NAME&for=county:*&in=state:{stateid}')
    result = json.loads(result.read())
    statename = result[1][0].split(',')[1].replace(' ','')
    time.sleep(.5)
    values = [[stateid, statename, x[2], x[0].split(',')[0].replace(' ','')] for x in result]
    conn = sqlite3.connect('census-information')
    curs = conn.cursor()
    curs.executemany(f'insert into {statename} values (?, ?, ?, ?)', values)
    conn.commit()

def create_counties():
    conn = sqlite3.connect('census-information')
    curs = conn.cursor()
    curs.execute('select * from states');
    states = curs.fetchall()
    for state in states:
        create_county_database(state[1].replace(' ',''))
        populate_county(f'{state[0]:02}')


'''
create table states(stateid int primary key, statename char(30));
create table counties(countyid int primary key, countyname char(30), stateid int, foreign key (stateid) references states(stateid));
create table rental_vacancies(year int, vacancy int, countyid int, foreign key (countyid) references counties (countyid));
'''
