import json
import os

from src.Parser_hh import Parser_hh

path_emp = os.path.join('employers.json')
path_vac = os.path.join('vacancies.json')


def get_data_from_hh_employers_and_vacancies(top, limiter):
    """ Получает данные о 10 работодателях и их вакансий с сайта hh.ru
        Название компании"""

    if os.path.exists(path_emp):
        os.remove(path_emp)

    if os.path.exists(path_vac):
        os.remove(path_vac)

    employers_all = []
    vacancies_all = []
    vacancies_valid = []


    for employer in top:
        hh = Parser_hh(employer, limiter)
        hh.get_employers_and_vacancies()
        employers_all.append(hh.employers)
        vacancies_all.append(hh.vacancies)
        for item_l in vacancies_all:
            for item in item_l:
                if item['salary'] is not None and item['address'] is not None:
                    vacancies_valid.append(item)
    with open(path_emp, "w", encoding='UTF-8') as file:
        json.dump(employers_all, file, ensure_ascii=False)
    with open(path_vac, "w", encoding='UTF-8') as file:
        json.dump(vacancies_valid, file, ensure_ascii=False)


def get_data_from_file(name_file):
    """Чтение файла и преобразует в json"""

    with open(name_file, "r", encoding='UTF-8') as read_file:
        data = json.load(read_file)
        return data
