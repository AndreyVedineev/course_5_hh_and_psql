import os

import psycopg2
from dotenv import load_dotenv

from src.DBManader import DBManager
from src.functions import get_data_from_file, get_data_from_hh_employers_and_vacancies

path_emp = os.path.join('employers.json')
path_vac = os.path.join('vacancies.json')
path_json = [path_emp, path_vac]
employers_top = ['Сбер', 'Яндекс', 'Альфа-банк', 'VK', 'Роснефть', 'ВТБ', 'Сибур', 'Почта России', 'МТС',
                 'Газпром']
limiter_of_the_number_of_vacancies = 2

load_dotenv()  # take environment variables from .env.

db_config = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT')
}


def main():
    name_db = 'vacancies_hh'
    get_data_from_hh_employers_and_vacancies(employers_top, limiter_of_the_number_of_vacancies)
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

    print("Список вакансий")
    list_of_vacancies = db.get_all_vacancies()
    for i in list_of_vacancies:
        print(f'Компания: {i["title"]} Вакансия: {i["name_vacancy"]} '
              f'Зарплата от: {i["salary_from"]} {i["currency"]} Ссылка: {i["vacancy_url"]}')

    currencies_list = db.get_currencies()
    for cur in currencies_list:
        avg_salary = db.get_avg_salary(cur)
        print(f'Средняя зарплата: Валюта: {cur} - {round(avg_salary, 2)}')

        higher_salary = db.get_vacancies_with_higher_salary(cur, avg_salary)
        print(f'Cписок всех вакансий, у которых зарплата выше средней по валюте {cur}')
        for hi in higher_salary:
            print(f'Вакансия: {hi["name_vacancy"]}, Заарплата от: {hi["salary_from"]}, ссылка: {hi["vacancy_url"]}')
    print("Введите ключевое слово для поиска по названию вакансий - ")
    # kw = input()
    kw = 'Инженер'
    vacancies_with_keyword = db.get_vacancies_with_keyword(kw)
    for vwk in vacancies_with_keyword:
        print(f'Вакансия: {vwk["name_vacancy"]}, Зарплата от: {vwk["salary_from"]}, ссылка: {vwk["vacancy_url"]}')


def _create_db(database_name: str, **params):
    """Создание базы данных"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    # Проверка наличия базы данных
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname=%s", [database_name])
    result = cur.fetchone()
    # Если база данных существует, выполняем операцию DROP DATABASE
    if result:
        cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    conn.close()


if __name__ == '__main__':
    main()
