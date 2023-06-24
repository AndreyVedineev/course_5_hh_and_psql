import os
import psycopg2

from dotenv import load_dotenv
from src.DBManader import DBManager
from src.functions import get_data_from_hh_employers_and_vacancies, get_data_from_file

path_emp = os.path.join('employers.json')
path_vac = os.path.join('vacancies.json')
path_json = [path_emp, path_vac]

load_dotenv()  # take environment variables from .env.

# db_config = {
#     'user': os.getenv('POSTGRES_USER'),
#     'password': os.getenv('POSTGRES_PASSWORD'),
#     'host': os.getenv('POSTGRES_HOST'),
#     'port': os.getenv('POSTGRES_PORT')
# }


def main():
    name_db = 'vacancies_hh'
    get_data_from_hh_employers_and_vacancies()
    _create_db(name_db, **db_config)
    db = DBManager(name_db, **db_config)
    data_emp = get_data_from_file(path_emp)
    for item_l in data_emp:
        for item in item_l:
            db.save_data_to_table_employers(item)

    data_vac = get_data_from_file(path_vac)
    for item_l in data_vac:
        db.save_data_to_table_vacancies(item_l)
    print(" Вакансии собраны и записаны в файл vacancies.json")


def _create_db(database_name: str, **params):
    """Создание базы данных"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    conn.close()


if __name__ == '__main__':
    main()
