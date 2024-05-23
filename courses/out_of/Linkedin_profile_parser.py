import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://www.linkedin.com/in/davidinmichael/'
linkedin_username = ''
linkedin_password = ''

driver = webdriver.Chrome()

driver.get('https://www.linkedin.com')
time.sleep(2)
driver.find_element(By.ID, 'session_key').send_keys(linkedin_username)
time.sleep(4)
driver.find_element(By.ID, 'session_password').send_keys(linkedin_password)
time.sleep(2)
driver.find_element(By.ID, 'session_password').send_keys(Keys.RETURN)
time.sleep(2)

driver.get(url)
try:
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')

    if soup:
        education_items = soup.find_all('a', class_='optional-action-target-wrapper')
        print(education_items)

        for item in education_items:
            academy_name = item.find('span', class_='t-bold').get_text(strip=True)
            degree_info = item.find('span', class_='t-14').get_text(strip=True)
            date_info = item.find('span', class_='t-black--light').get_text(strip=True)

            print("Academy:", academy_name)
            print("Degree Info:", degree_info)
            print("Date Info:", date_info)
            print()

    else:
        print('Education section not found.')

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()
