import sqlite3
import sys

def get_tables(arg):
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    sqlTxn = f'select name from sqlite_master where type = \'table\' and name like \'{arg}%\''
    tables = curs.execute(sqlTxn)
    conn.commit()
    return [table[0] for table in tables.fetchall()]

def get_linear_growth(table):
    conn = sqlite3.connect('census-information.db')
    curs = conn.cursor()
    sqlTxn = f'select * from {table} order by year'
    results = curs.execute(sqlTxn)
    conn.commit()
    return [line for line in results.fetchall()]

if __name__ == '__main__':
    print(sys.argv)
    print(sys.argv[1:])
    if sys.argv[1:] == []:
        for l in get_linear_growth(get_tables('B07001_022E')[0]):
            print(l)
