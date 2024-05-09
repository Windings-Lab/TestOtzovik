import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        driver = webdriver.Chrome()
        driver.get(url)
        html_content = driver.page_source
        driver.quit()
        return html_content


def make_soup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    if soup:
        return soup


def parse_soup(soup):
    if soup:
        course_title_tag = soup.find('h1', {'class': 'display-2', 'itemprop': 'name'})
        course_title = course_title_tag.text.strip() if course_title_tag else None

        price_tag = soup.find('b', {'class': 'fs-22'})
        price = price_tag.text if price_tag else None

        company_pattern = re.compile(r'/courses/company/\d+/')
        company_tag = soup.find('a', {'href': company_pattern})
        company = company_tag.text if company_tag else None

        group_tag = soup.find('span', {'class': 'glyphicon glyphicon-age-group'})
        group = group_tag.find_next_sibling('span').text if group_tag else None

        location_tag = soup.find('span', {'class': 'glyphicon glyphicon-location'})
        location = location_tag.find_next('a').text if location_tag else None

        website_tag = soup.find('span', {'class': 'glyphicon glyphicon-website'})
        website = website_tag.find_next('span').text if website_tag else None

        contact_tag = soup.find('span', {'class': 'glyphicon glyphicon-contact'})
        contact = contact_tag.find_next('span').text if contact_tag else None

        description_tag = soup.find('div', {'itemprop': 'description'})
        description = description_tag.text.strip() if description_tag else None

        return course_title, price, company, group, location, website, contact, description


def fetch_max_page_number():
    html_content = fetch_data('https://www.education.ua/courses/?search=&city=0&kind=0')
    soup = BeautifulSoup(html_content, 'html.parser')

    page_link = soup.find_all('a', class_='page-link')
    max_number = page_link[2].text.split('=')[-1]
    return int(max_number)


def links_pagination():
    max_number = fetch_max_page_number()
    links = []
    for page in range(1, max_number + 1):
        link = f'https://www.education.ua/courses/?search=&city=0&kind=0&page={page}'

        links.append(link)
    return links


def fetch_courses_links(soup):
    if soup:
        course_cards = soup.find_all('div', class_='card')
        links = []
        for card in course_cards:
            a_tag = card.find('h2')
            if a_tag:
                a_tag = a_tag.find('a')
                href = a_tag['href']
                full_href = 'https://www.education.ua/' + href
                links.append(full_href)
        return links


def total_links():
    total = []
    links = links_pagination()
    for link in links:
        soup = make_soup(html_content=fetch_data(link))
        courses_links = fetch_courses_links(soup)
        for course in courses_links:
            total.append(course)
    return total


def main():
    fetch_max_page_number()


if __name__ == '__main__':
    main()
