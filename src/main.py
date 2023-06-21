import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

db_config = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'dbname': os.getenv('POSTGRES_DB')
}


def main():
    pass


if __name__ == '__main__':
    main()
