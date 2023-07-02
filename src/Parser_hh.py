import os

import requests


class ConnectionErrors(BaseException):
    """Класс исключения при отсутствии кода скрипта"""

    def __init__(self):
        self.message = 'Ошибка соединения. Код ответа не равен 200'

    def __str__(self):
        return self.message


class Parser_hh:
    """
    Получает данные о работодателях и их вакансий с сайта hh.ru
    """

    def __init__(self, top_employer: str, depth_of_vacancies):
        self.top_employer = top_employer  # ключевое слово для поиска
        self.page_number = 0
        self.url_emp = 'https://api.hh.ru/employers?'
        self.url_vac = None
        self.min_payment = 0
        self.token = os.getenv("token")
        self.employers = []
        self.vacancies = []
        self.depth_of_vacancies = depth_of_vacancies

    def get_employers_and_vacancies(self):
        """ Создание файла с работодателями
            Создание файла с вакансиями работодателей """

        params_emp = {'text': self.top_employer,
                      'only_with_vacancies': True,
                      'page': self.page_number,
                      'per_page': 20}

        headers = {'User-Agent': 'K_ParserApp/1.0',
                   'Authorization': f'Bearer {self.token}'}

        response = requests.get(self.url_emp, params=params_emp, headers=headers)
        if response.status_code != 200:
            raise ConnectionErrors

        count_data = response.json()['pages']

        for i in range(count_data):
            param_cycle_emp = {'text': self.top_employer,
                               'only_with_vacancies': True,
                               'page': i}
            response_cycle = requests.get(self.url_emp, params=param_cycle_emp, headers=headers)
            result = response_cycle.json()
            self.employers.extend(result['items'])

        for item in self.employers:
            print(f"Забирою вакансии {item['name']} с сайта HH")
            if item['open_vacancies'] < self.depth_of_vacancies:
                self.url_vac = item['vacancies_url']
                response = requests.get(self.url_vac, headers=headers)
                count_data = response.json()['pages']
                for i in range(count_data):
                    param_cycle_vac = {'page': i}
                    response_cycle = requests.get(self.url_vac, params=param_cycle_vac, headers=headers)
                    result = response_cycle.json()
                    self.vacancies.extend(result['items'])

    def __str__(self):
        return self
