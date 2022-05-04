import time
import csv
import math
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import random

data = []
record_added = 0
START_INDEX = 100
END_INDEX = 80

URL = 'https://partnercarrier.com/TX'
NO_OF_RECORDS_PER_PAGE = 70
FILE_NAME = 'Texas_1.csv'
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(URL)


def add_random_wait():
    wait_time = random.uniform(0.1, 0.9)
    print("Waiting for - {} secs".format(wait_time))
    time.sleep(wait_time)


def load_pages(_driver, p_url, page_records):
    add_random_wait()
    driver.get(p_url)
    for x in range(2, (page_records+2)):
        try:
            abc = '//*[@id="companyList"]/div[{}]/div/div[2]/div/div[4]/a'.format(x)
            p = _driver.find_element_by_xpath(abc)
            # add_random_wait()
            time.sleep(random.uniform(1, 2))
            p.click()
            retrieve_single_company_data(driver)
        except Exception as e:
            print(e)
    driver.back()


def retrieve_single_company_data(_driver):
    try:
        name = driver.find_element_by_xpath('//h2[@class="text-center"]').text
        container_1 = driver.find_elements_by_xpath("//div[@class='col-sm-4 col-md-4 nopadding-left']")
        address = container_1[0].text.split(':')[1][1::]
        phone = container_1[1].text.split(':')[1]

        container_2 = driver.find_elements_by_xpath("//div[@class='col-sm-4 nopadding-left']")
        trucks = int(container_2[3].text.split(':')[1])
        cell = container_2[5].text.split(':')[1]
        email = container_2[7].text.split(':')[1]
        website = container_2[8].text.split(':')[1]

        if 0 < trucks <= 5:
            print(name, address, phone, cell, email, website, trucks)
            write_to_csv([name, address, phone, cell, email, website, trucks])
    except Exception as e:
        print(e)
    _driver.back()


def create_csv_title():
    if os.path.isfile(FILE_NAME):
        return
    f = open(FILE_NAME, 'a')
    writer = csv.writer(f)
    writer.writerow(("Name", 'Address', "Phone", "Cell", "Email", "Website", "Trucks"))

    f.close()


def write_to_csv(fields):
    with open(FILE_NAME, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)


links = driver.find_elements_by_class_name('city-link-font-size')

cities_links = [link.get_attribute('href') for link in links[START_INDEX:END_INDEX]]
create_csv_title()

for city_link in cities_links:
    try:
        add_random_wait()
        page_url = city_link
        driver.get(page_url)
        total_records = int(driver.find_elements_by_xpath('//text[@class="total-companies"]')[0].text)
        if total_records > NO_OF_RECORDS_PER_PAGE:
            page_count = int(math.ceil(total_records/NO_OF_RECORDS_PER_PAGE))
        else:
            page_count = 1
        remaining_records = total_records
        current = NO_OF_RECORDS_PER_PAGE if page_count > 1 else total_records
    except Exception as e:
        print(e)
    for k in range(1, page_count+1):
        paginated_url = page_url + "?p={}".format(k)
        load_pages(driver, paginated_url, page_records=current)
        remaining_records = remaining_records - current
        add_random_wait()
# driver.back()

driver.close()
print("****data added successfully*****")
