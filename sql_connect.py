import sqlite3

class sql_connect:
    def __init__(self, func):
        self.conn = sqlite3.connect('census-information.db')
        self.curs = self.conn.cursor()
        self.func = func
    def __call__(self, *args):
        self.func(self.curs, *args)
        self.conn.commit()


@sql_connect
def get_states(curs):
    states = curs.execute('select * from states')
    print(states.fetchall())

if __name__ == '__main__':
    get_states()
