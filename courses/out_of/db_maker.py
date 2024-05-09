import sqlite3
import os
import django
from django.conf import settings
from courses_parser import parse_soup, total_links, fetch_data, make_soup
# from courses.models import Course


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "otzovik.otzovik.settings")

django.setup()


def insert_course(course_data):
    conn = sqlite3.connect(settings.DATABASES['default']['NAME'])
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM courses_course WHERE title = ? AND company = ?", (course_data[0], course_data[2]))
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute('''INSERT INTO courses_course 
                          (title, price, company, age, location, website, contact, description, time_added, time_updated) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, DATETIME('now'), DATETIME('now'))''', course_data)
        conn.commit()
    else:
        print(f"Duplicate entry: {course_data[0]} - {course_data[2]}")

    cursor.close()
    conn.close()


for link in total_links():
    soup = make_soup(fetch_data(link))
    db_data = parse_soup(soup)
    insert_course(db_data)


# from courses.models import Course

# def insert_course(course_data):
#     title, price, company, age, location, website, contact, description = course_data
#     Course.objects.get_or_create(
#         title=title,
#         price=price,
#         company=company,
#         age=age,
#         location=location,
#         website=website,
#         contact=contact,
#         description=description,
#     )

