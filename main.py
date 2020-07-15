import sys
import os
import pathlib
import csv
import database as db
import census_api as c

#global variables for paths
dirpath = pathlib.Path().absolute()
table_location = os.path.join(dirpath, 'table_variables')
variables = os.walk(table_location)

#returns the csv files saved the the table_variables directory
def get_tables():
    csv_files = []
    for _, _, tables in variables:
        [csv_files.append(x) for x in tables if '.csv' in x]
    return csv_files

def get_results(table, i, year, data):
    data_set = ','.join([f'{x} char' for x in data])
    api_set = ','.join([f'{x}' for x in data])
    census_call = c.get_table(f'{table}.csv')
    try:
        results = census_call(api_set, year) 
        for r in results[1:]:
            countyid = r[-1]
            stateid = r[-2]
            tablename = f'{table}_{stateid}_{countyid}_{i}'
            if tablename not in db.get_tables():
                db.create_data_table(tablename, stateid, countyid, data_set)
                data_package = [[data[i], r[i]] for i in range(len(data))]
                db.populate_dataset(tablename, stateid, countyid, data_package, year)
    except:
        pass
        

#iterate through all years 
def iterate_through_years(table, i, data):
    for year in range(2011, 2019):
        get_results(table, i, year, data)

def create_variable_chunks(data, table):
    rows_iter = [data[i:i+50] for i in range(0, len(data), 50)]
    for i, row in enumerate(rows_iter):
        print(f'{table} iteration {i}')
        iterate_through_years(table.replace('.csv',''), i, row)

#opens a csv file and creates 
def open_table(table):
    csv_file = open(os.path.join(table_location, table), 'r')
    csv_reader = csv.reader(csv_file, delimiter=',')
    csv_rows = [r[0] for r in csv_reader if r[1] is not 'string'] #removes string from rows
    create_variable_chunks(csv_rows, table)

if __name__ == '__main__':
    csv_files = get_tables()
    args = sys.argv[1:] if len(sys.argv) else None
    if args:
        pass
    else:
        for table in csv_files:
            data = open_table(table)
