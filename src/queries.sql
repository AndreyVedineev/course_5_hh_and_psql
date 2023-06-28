CREATE TABLE IF NOT EXISTS {self.table_1} (
                                id SERIAL  PRIMARY KEY,
                                employee_id VARCHAR(10),
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

SELECT * FROM employers;

SELECT * FROM vacancies;


SELECT title, name_vacancy, salary_from, currency, vacancy_url FROM vacancies
FULL JOIN employers USING(employee_id)
ORDER BY salary_from;

SELECT AVG (salary_from) FROM vacancies;

SELECT COUNT(currency) FROM vacancies;

SELECT DISTINCT currency FROM vacancies;


SELECT name_vacancy, salary_from, vacancy_url FROM vacancies WHERE currency = 'KZT' GROUP BY id
HAVING salary_from > (SELECT AVG (salary_from) FROM vacancies);


SELECT name_vacancy, salary_from, vacancy_url FROM vacancies
WHERE name_vacancy LIKE ('%Инженер%');