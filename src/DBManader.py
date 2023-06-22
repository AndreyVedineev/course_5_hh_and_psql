import psycopg2


class DBManager:
    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost',
                 port: str = '5432'):
        self.table_1 = 'employers'
        self.table_2 = 'vacancies'
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        pass
