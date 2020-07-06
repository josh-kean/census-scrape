import sqlite3
import time
import urllib.request as url
import json

api_key = 'a15f9f0e3cc9f5d60e635e55a58a73104ff52fe3'

#three databases for now; states and their state id
#counties for each state
#vacancies per county per year

def get_tables():
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    tables = curs.execute('select name from sqlite_master where type = \'table\'')
    conn.commit()
    return [table[0] for table in tables.fetchall()]

def get_states():
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    states = curs.execute('select * from states')
    conn.commit()
    return states.fetchall()

def get_counties(state):
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    counties = curs.execute(f'select * from {state}')
    return counties.fetchall()

def create_dataset(table_name, stateid):
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    sqlTxn = f'create table if not exists {table_name}(year int, data char, countyid int, stateid int, foreign key (stateid) references states(stateid))'
    curs.execute(sqlTxn)
    conn.commit()

def populate_dataset(table_name, data):
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    curs.execute(f'insert into {table_name} values(?,?,?,?)', (int(data[0]), data[1],int(data[2]), int(data[3])))
    conn.commit()

def create_state_database(stateid, statename):
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    curs.execute('insert into states values(?, ?)', (int(stateid), statename))
    conn.commit()

def create_county_database(statename):
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    sqltxn = f'create table if not exists {statename}(stateid int, statename char, countyid int primary key, countyname text, foreign key (stateid) references states(stateid))'
    curs.execute(sqltxn)
    conn.commit()

def create_states():
    conn = sqlite3.connect('census-information.db')
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
            create_state_database(stateid, statename.replace(' ',''))
            time.sleep(.5)
        except:
            print(f'{x} state failed')


def populate_county(stateid):
    result = url.urlopen(f'https://api.census.gov/data/2018/acs/acs1/cprofile?get=NAME&for=county:*&in=state:{stateid}')
    result = json.loads(result.read())
    statename = result[1][0].split(',')[1].replace(' ','')
    time.sleep(.5)
    values = [[stateid, statename, x[2], x[0].split(',')[0].replace(' ','').replace('-','')] for x in result]
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    curs.executemany(f'insert into {statename} values (?, ?, ?, ?)', values)
    conn.commit()

def create_counties():
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    curs.execute('select * from states');
    states = curs.fetchall()
    for state in states:
        create_county_database(state[1].replace(' ',''))
        populate_county(f'{state[0]:02}')

