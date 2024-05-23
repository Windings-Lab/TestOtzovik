import os

import django
import psycopg2
from courses_parser import fetch_data, make_soup, parse_soup, total_links
from django.conf import settings

from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv('azure.env')

if ENV_FILE:
    load_dotenv(ENV_FILE)


DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_HOST = os.environ.get('DB_HOST')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "otzovik.otzovik.settings")
django.setup()


def insert_course(course_data):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=5432
    )
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM courses_course WHERE title = %s AND company = %s", (course_data[0], course_data[2]))
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute('''INSERT INTO courses_course 
                          (title, price, company, age, location, website, contact, description, time_added, time_updated) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)''', course_data)
        conn.commit()
    else:
        print(f"Duplicate entry: {course_data[0]} - {course_data[2]}")

    cursor.close()
    conn.close()


def main():
    for link in total_links():
        soup = make_soup(fetch_data(link))
        db_data = parse_soup(soup)
        insert_course(db_data)


if __name__ == '__main__':
    main()
