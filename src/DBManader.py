from typing import Any

import psycopg2


class DBManager:
    """ Работает с БД vacancies_hh"""

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
                                id SERIAL  PRIMARY KEY,
                                employee_id VARCHAR(10)
                                title VARCHAR(200),
                                url_api VARCHAR(200),
                                alternate_url VARCHAR(200),
                                vacancies_url VARCHAR(200)
                                );
                                CREATE TABLE IF NOT EXISTS {self.table_2} (
                                id SERIAL  PRIMARY KEY,
                                vacancy_id VARCHAR(10),
                                employee_id VARCHAR(10),
                                name_vacancy VARCHAR(200),
                                name_area VARCHAR(70),
                                salary_from INTEGER,
                                salary_to VARCHAR(10) DEFAULT NULL,
                                currency VARCHAR(3) DEFAULT NULL,
                                published_at VARCHAR(24),
                                vacancy_url VARCHAR(200),
                                requirement text,
                                responsibility text
                                );
                                 """)

    def save_data_to_table_employers(self, data: dict):
        """Заполняет таблицу employers данными из файла employers.json """
        self.cur.execute(
            f'INSERT INTO {self.table_1} (employee_id, title, url_api, alternate_url, vacancies_url)'
            f'VALUES (%s, %s, %s, %s, %s)', (data['id'], data['name'], data['url'], data['alternate_url'],
                                             data['vacancies_url'])
        )

    def save_data_to_table_vacancies(self, data: dict):
        """Заполняет таблицу vacancies данными из файла vacancies.json """
        self.cur.execute(
            f'INSERT INTO {self.table_2} (vacancy_id, employee_id, name_vacancy, name_area, salary_from,'
            f'salary_to, currency, published_at, vacancy_url, requirement, responsibility )'
            f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (data['id'], data['employer']['id'], data['name'], data['address']['city'], data['salary']['from'],
             data['salary']['to'],
             data['salary']['currency'], data['published_at'], data['alternate_url'],
             data['snippet']['requirement'], data['snippet']['responsibility'])
        )

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии изарплаты и ссылки на
        вакансию."""
        self.cur.execute(f'SELECT title, name_vacancy, salary_from, currency, vacancy_url FROM vacancies '
                         f'JOIN employers USING(employee_id) ORDER BY name_vacancy')
        data = self.cur.fetchall()
        data_list = [{"title": d[0], "name_vacancy": d[1], "salary_from": d[2], "currency": d[3], "vacancy_url": d[4]}
                     for d in data]
        return data_list

    def get_avg_salary(self, cur):
        """Получает среднюю зарплату по вакансиям."""
        self.cur.execute('SELECT AVG (salary_from) FROM vacancies WHERE currency=%s', [cur])
        return self.cur.fetchone()[0]

    def get_currencies(self):
        """Получает список валют"""
        self.cur.execute(f'SELECT DISTINCT currency FROM vacancies')
        data = self.cur.fetchall()
        data_list = [d[0] for d in data]
        return data_list

    def get_vacancies_with_higher_salary(self, cur, avg):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        self.cur.execute("""SELECT name_vacancy, salary_from, vacancy_url FROM vacancies 
                            WHERE currency = %(cur)s 
                            GROUP BY id 
                            HAVING salary_from > %(avg)s""", {'cur': cur, 'avg': avg})
        data = self.cur.fetchall()
        data_list = [{"name_vacancy": d[0], "salary_from": d[1], "vacancy_url": d[2]} for d in data]
        return data_list

    def get_vacancies_with_keyword(self, kw):
        """Получает список всех вакансий, в названии которых содержатся слова, например “python”."""
        self.cur.execute(f"SELECT name_vacancy, salary_from, vacancy_url "
                         f"FROM vacancies WHERE name_vacancy "
                         f"LIKE '%{kw}%'")
        data = self.cur.fetchall()
        data_list = [{"name_vacancy": d[0], "salary_from": d[1], "vacancy_url": d[2]} for d in data]
        return data_list

    def __str__(self):
        return self
