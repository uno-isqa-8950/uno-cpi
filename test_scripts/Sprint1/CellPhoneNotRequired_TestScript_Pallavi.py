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
        driver.get("http://127.0.0.1:8000/partners/registerCommunityPartner/")
        time.sleep(1)
        elem = driver.find_element_by_xpath('//*[@id="id_name"]')
        elem.send_keys('Very Helpful Society')  #After every test, put a different name here
        time.sleep(1)
        elem = driver.find_element_by_xpath('//*[@id="id_website_url"]')
        elem.send_keys('www.uno.com')
        select = Select(driver.find_element_by_id('id_community_type'))
        select.select_by_index(3)
        elem = driver.find_element_by_xpath('//*[@id="id_address_line1"]')
        elem.send_keys('70th Plaza ')
        elem = driver.find_element_by_xpath('//*[@id="id_city"]')
        elem.send_keys('Omaha')
        elem = driver.find_element_by_xpath('//*[@id="id_state"]')
        elem.send_keys('Nebraska')
        elem = driver.find_element_by_xpath('//*[@id="id_zip"]')
        elem.send_keys('68106')
        elem = driver.find_element_by_xpath('//*[@id="id_country"]')
        elem.send_keys('USA')
        select = Select(driver.find_element_by_id('id_contact-0-contact_type'))
        select.select_by_index(1)
        elem = driver.find_element_by_xpath('//*[@id="id_contact-0-email_id"]')
        elem.send_keys('p1994@unomaha.edu')
        elem = driver.find_element_by_xpath('//*[@id="id_contact-0-first_name"]')
        elem.send_keys('Pallavi')
        elem = driver.find_element_by_xpath('//*[@id="id_contact-0-last_name"]')
        elem.send_keys('Chauhan')
        elem = driver.find_element_by_xpath('//*[@id="id_contact-0-work_phone"]')
        elem.send_keys('1234567890')
        select = Select(driver.find_element_by_id('id_mission-0-mission_type'))
        select.select_by_index(1)
        time.sleep(5)
        select = Select(driver.find_element_by_id('id_mission-0-mission_area'))
        select.select_by_index(3)
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/form/div[4]/div/button').click()
        time.sleep(4)




    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
