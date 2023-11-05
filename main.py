from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import csv


options = webdriver.ChromeOptions()
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
options.add_argument('--disable-blink-features=AutomationControlled')

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15, poll_frequency=1)


with open('companies.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(
        (
          'Company',
          'Name',
          'Title',
          'Email',
          'Address1',
          'Address2',
          'Address3',
          'Phone'

        )
    )



driver.get('https://www.dataprivacyframework.gov/s/participant-search')
time.sleep(4)




for i in range(1, 377):
    for card_numb in range(11, 21):
        
        ACT = ('xpath', '//li[@title="INACTIVE"]')
        wait.until(EC.visibility_of_element_located(ACT))
        driver.find_element('xpath', '//li[@title="INACTIVE"]').click()

        ENTRY = (By.XPATH, f'(//*[@class="slds-text-heading_small lgorg"])[{card_numb}]')
        wait.until(EC.visibility_of_element_located(ENTRY))
        time.sleep(0.5)
        card_entry = driver.find_element(By.XPATH, f'(//*[@class="slds-text-heading_small lgorg"])[{card_numb}]').click()

        ELEMENT_VISIBLE = ('xpath', '//*[@class="slds-col slds-size_6-of-12 lginside"]')
        wait.until(EC.visibility_of_element_located(ELEMENT_VISIBLE))

        soup = BeautifulSoup(driver.page_source, 'lxml')

        all_blocks = soup.find_all('div', class_='slds-col slds-size_6-of-12 lginside')

        company = soup.find('h2', class_='slds-nav-vertical__title').text

        first_block = all_blocks[-2]
        value = first_block.find_all('div')
        name = value[0].text
        title = value[1].text
        address_1 = value[2].text
        address_2 = value[3].text
        address_3 = value[4].text

        second_block = all_blocks[-1]
        second_value = second_block.find_all('div')
        email = second_value[0].find('a').text
        number = second_value[1].find('a').text
        time.sleep(1)
        
        with open('companies.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                company,
                name,
                title,
                email,
                address_1,
                address_2,
                address_3,
                number

                )
            )



        driver.back()

        if card_numb == 20:
            ACT = ('xpath', '//li[@title="INACTIVE"]')
            wait.until(EC.visibility_of_element_located(ACT))
            driver.find_element('xpath', '//li[@title="INACTIVE"]').click()

            NEXT = ('xpath', '//*[@id="tab-2"]/slot/c-partcipant-list-component/div[4]/c-pagination/lightning-layout/slot/lightning-layout-item[3]')
            wait.until(EC.visibility_of_element_located(NEXT))
            driver.find_element('xpath', '//*[@id="tab-2"]/slot/c-partcipant-list-component/div[4]/c-pagination/lightning-layout/slot/lightning-layout-item[3]').click()



    print(f'[INFO]  Страница №{i} из 377 - обработана')
        
