import os

from dotenv import load_dotenv

from src.Parser_hh import Parser_hh

path_emp = os.path.join('employers.json')
path_vac = os.path.join('vacancies.json')


def get_data_from_hh_employers_and_vacancies():
    """ Получает данные о 10 работодателях и их вакансий с сайта hh.ru
        Название компании - топ сайта hh.ru 2022 года """

    if os.path.exists(path_emp):
        os.remove(path_emp)

    if os.path.exists(path_vac):
        os.remove(path_vac)

    employers_top = ['Сбер', 'Яндекс', 'Альфа-банк', 'VK', 'Газпром-нефть', 'ВТБ', 'Сибур', 'Tele2', 'МТС',
                     'Газпромбанк']
    for employer in employers_top:
        hh = Parser_hh(employer)
        hh.get_employers_and_vacancies()
