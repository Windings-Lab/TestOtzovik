import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://www.linkedin.com/in/davidinmichael/'

linkedin_username = 'username'
linkedin_password = 'password'

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
    education_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'tLzAqgOsJVrYZstVCPtfORDEWStVfVLul'))
    )

    html_content = driver.page_source
    with open('some.txt', 'w', encoding='utf-8') as file:
        file.write(html_content)
        print('HTML content written to file.')

    soup = BeautifulSoup(html_content, 'html.parser')
    education = soup.find('div', class_='education-section')

    if education:
        spans_with_aria_hidden_true = education.find_all('span', attrs={'aria-hidden': 'true'})

        for span in spans_with_aria_hidden_true:
            text_content = span.get_text(strip=True)
            print("Text content:", text_content)
    else:
        print('Education div not found.')

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()
