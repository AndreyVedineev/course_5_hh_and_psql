from typing import Any

import psycopg2


class DBManager:
    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost',
                 port: str = '5432'):
        self.table_1 = 'employers'
        self.table_2 = 'vacancies'
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()
        self.dbname = dbname
        self.conn.autocommit = True
        self._create_tables()

    def _create_tables(self):
        """Создание таблиц для сохранения данных о вакансиях"""
        with self.conn:
            self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_1} (
                                employee_id VARCHAR(10) PRIMARY KEY,
                                title VARCHAR(100),
                                url_api VARCHAR(100),
                                alternate_url VARCHAR(100),
                                vacancies_url VARCHAR(100)
                                );
                                CREATE TABLE IF NOT EXISTS {self.table_2} (
                                id SERIAL  PRIMARY KEY,
                                vacancy_id VARCHAR(10),
                                employee_id VARCHAR(10),
                                name_vacancy VARCHAR(100),
                                name_area VARCHAR(70),
                                salary_from VARCHAR(10) DEFAULT NULL,
                                salary_to VARCHAR(10) DEFAULT NULL,
                                currency VARCHAR(3) DEFAULT NULL,
                                published_at VARCHAR(24),
                                vacancy_url VARCHAR(100),
                                requirement text,
                                responsibility text
                                );
                                 """)

    def save_data_to_table_employers(self, data: dict):
        self.cur.execute(
            f'INSERT INTO {self.table_1} (employee_id, title, url_api, alternate_url, vacancies_url)'
            f'VALUES (%s, %s, %s, %s, %s)', (data['id'], data['name'], data['url'], data['alternate_url'],
                                             data['vacancies_url'])
        )

    def save_data_to_table_vacancies(self, data: dict):
        self.cur.execute(
            f'INSERT INTO {self.table_2} (vacancy_id, employee_id, name_vacancy, name_area, salary_from,'
            f'salary_to, currency, published_at, vacancy_url, requirement, responsibility )'
            f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (data['id'], data['employer']['id'], data['name'], data['address']['city'], data['salary']['from'],
             data['salary']['to'], data['salary']['currency'], data['published_at'], data['alternate_url'],
             data['snippet']['requirement'], data['snippet']['responsibility'])
        )

    def __str__(self):
        return self
