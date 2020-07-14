'''
this provides functionality to search the sql databases and find relevant information
'''

import csv
import sqlite3
import urllib
import sys
from sql_connect import database_connect as dc

#get all tables of a certain prefix
@dc
def get_tables(curs, arg):
    sqlTxn = f'select name from sqlite_master where type = \'table\' and name like \'{arg}%\''
    try:
        tables = curs.execute(sqlTxn)
    except Exception as e:
        pass
    return [table[0] for table in tables.fetchall()]

#calculate the growth of a table
#the math sucks in the definition, make it better
@dc
def get_linear_growth(curs, table):
    curs = conn.cursor()
    sqlTxn = f'select distinct * from {table} order by year '
    try:
        results = curs.execute(sqlTxn)
        conn.commit()
        return [line for line in results.fetchall()]
    except:
        return [f'{table} not valid']

#creates a csv file of all the analyzed information
def create_csv(data, name):
    data_file = open(f'{name}.csv', 'a', newline='')
    writer = csv.writer(data_file, delimiter=',')
    writer.writerow(data)



if __name__ == '__main__':
    if sys.argv[1:] == []:
        tables = get_tables('DP04_0089E')
        costs = []
        for i, table in enumerate(tables):
            print(len(tables)-i)
            result = get_linear_growth(table)
            if len(result) == 1:
                continue
            prices = [int(x[1]) for x in result if int(x[1]) > 0]
            diff = max(prices)-min(prices) 
            create_csv([table, diff, result[0][2], result[0][3]], 'DP04_0089E')
