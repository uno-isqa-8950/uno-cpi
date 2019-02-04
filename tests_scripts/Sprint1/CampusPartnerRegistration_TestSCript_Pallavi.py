import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


class UnoCpi(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='C:\TESTING/chromedriver.exe')

    def test_website(self):
        user = "pallavichauhan@unomaha.edu"
        pwd = "1p2p3p4p5p"
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/a").click()
        driver.get("http://127.0.0.1:8000/partners/registerCampusPartner/")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//*[@id='id_name']")
        elem.send_keys('HPER')  #After every test, put a different name here
        time.sleep(1)
        select = Select(driver.find_element_by_id('id_college_name'))
        select.select_by_index(1)
        select = Select(driver.find_element_by_id('id_form-0-contact_type'))
        select.select_by_index(2)
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-email_id"]')
        elem.send_keys('pallavi@unomaha.edu')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-first_name"]')
        elem.send_keys('Pallavi')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-last_name"]')
        elem.send_keys('Chauhan')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-work_phone"]')
        elem.send_keys('1234567890')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-cell_phone"]')
        elem.send_keys('0987654321')
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/form/div/div/div[5]/div/button').click()
        time.sleep(1)
        driver.get('http://127.0.0.1:8000/admin/login/?next=/admin/')
        elem = driver.find_element_by_xpath('//*[@id="id_username"]')
        elem.send_keys(user)
        elem = driver.find_element_by_xpath('//*[@id="id_password"]')
        elem.send_keys(pwd)
        elem = driver.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').click()
        elem = driver.find_element_by_xpath('//*[@id="content-main"]/div[3]/table/tbody/tr[2]/th/a').click()
        time.sleep(7)


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
