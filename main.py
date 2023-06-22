import os
from dotenv import load_dotenv

from src.DBManader import DBManager

from src.functions import get_data_from_hh_employers_and_vacancies

load_dotenv()  # take environment variables from .env.

db_config = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'dbname': os.getenv('POSTGRES_DB')
}


def main():
    get_data_from_hh_employers_and_vacancies()
    # db = DBManager(**db_config)


if __name__ == '__main__':
    main()
