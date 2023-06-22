import json
import os

import requests

from fake_user_agent import user_agent

path_emp = os.path.join('employers.json')
path_vac = os.path.join('vacancies.json')


class Parser_hh:
    """
    Получает данные о работодателях и их вакансий с сайта hh.ru
    """

    def __init__(self, top_employer: str):
        self.top_employer = top_employer  # ключевое слово для поиска
        self.page_number = 0
        self.url_emp = 'https://api.hh.ru/employers?'
        self.url_vac = None
        self.min_payment = 0

    def get_employers_and_vacancies(self):
        """ Создание файла с работодателями
            Создание файла с вакансиями работодателей """

        employers = []
        vacancies = []
        params_emp = {'text': self.top_employer,
                      'only_with_vacancies': True,
                      'page': self.page_number,
                      'per_page': 20}

        # headers = {'User-Agent': user_agent('chrome'), 'Authorization': f'Bearer {access_token}'}

        headers = {'User-Agent': 'K_ParserApp/1.0',
                   'Authorization': 'Bearer APPLNO6F3AB2J9KNKSF33TOPP1EKGDRM9P16C1ED315I1D4E2RAIKI3R9JP1130K'}

        response = requests.get(self.url_emp, params=params_emp, headers=headers)
        count_data = response.json()['pages']
        for i in range(count_data):
            param_cycle = {'text': self.top_employer,
                           'only_with_vacancies': True,
                           'page': i}
            response_cycle = requests.get(self.url_emp, params=param_cycle, headers=headers)
            # print(f'Запрос к {self.top_employer} на  сайте HeadHunter')
            result = response_cycle.json()
            employers.extend(result['items'])
            # employers_sort = sorted(employers, key=lambda x: x['open_vacancies'], reverse=True)
            f = open(path_emp, mode='a', encoding='utf8')
            f.write(json.dumps(employers, ensure_ascii=False))
            f.close()

        for item in employers:
            if item['open_vacancies'] < 5:  # ограничитель количества вакансий 400
                self.url_vac = item['vacancies_url']
                response = requests.get(self.url_vac, headers=headers)
                count_data = response.json()['pages']
                for i in range(count_data):
                    param_cycle = {'page': i}
                    response_cycle = requests.get(self.url_vac, params=param_cycle, headers=headers)
                    result = response_cycle.json()

                    print(self.url_vac)
                    vacancies.extend(result['items'])
                    f = open(path_vac, mode='a', encoding='utf8')
                    f.write(json.dumps(vacancies, ensure_ascii=False))
                    f.close()

    def __str__(self):
        return self
