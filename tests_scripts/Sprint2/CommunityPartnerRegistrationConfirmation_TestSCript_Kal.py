import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


class UnoCpi(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='C:\Webdrivers/chromedriver.exe')

    def test_website(self):

        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/login/")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/a").click()
        driver.get("http://127.0.0.1:8000/partners/registerCommunityPartner/")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//*[@id='id_name']")
        elem.send_keys('TEST')
        elem = driver.find_element_by_xpath("//*[@id='id_website_url']")
        elem.send_keys('http://www.google.com')
        driver.find_element_by_xpath("//*[@id='id_community_type']/option[4]").click()
        elem = driver.find_element_by_xpath("//*[@id='id_address_line1']")
        elem.send_keys('171 Q st')
        elem = driver.find_element_by_xpath("//*[@id='id_city']")
        elem.send_keys('Omaha')
        elem = driver.find_element_by_xpath("//*[@id='id_state']")
        elem.send_keys('NE')
        elem = driver.find_element_by_xpath("//*[@id='id_zip']")
        elem.send_keys('68135')
        elem = driver.find_element_by_xpath("//*[@id='id_country']")
        elem.send_keys('USA')
        driver.find_element_by_xpath("//*[@id='id_contact-0-contact_type']/option[1]")
        elem = driver.find_element_by_xpath("//*[@id='id_contact-0-email_id']")
        elem.send_keys('test@test.edu')
        time.sleep(5)
        elem = driver.find_element_by_id('id_contact-0-first_name')
        elem.send_keys('tester')
        time.sleep(5)
        elem = driver.find_element_by_id('id_contact-0-last_name')
        elem.send_keys('test')
        elem = driver.find_element_by_id('id_contact-0-work_phone')
        elem.send_keys('1234567890')
        driver.find_element_by_xpath("//*[@id='id_mission-0-mission_type']/option[1]").click()
        driver.find_element_by_xpath("//*[@id='id_mission-0-mission_area']/option[5]").click()
        time.sleep(5)

        driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div[2]/form/div[4]/div/button").click()
        time.sleep(4)


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
