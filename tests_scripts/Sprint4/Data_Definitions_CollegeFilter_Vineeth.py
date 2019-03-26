import unittest
import time
from selenium import webdriver


class UnoCpi(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()


    def test_website(self):
        user = "email@gmail.com"
        pwd = "Password"
        driver = self.driver
        driver.maximize_window()
        driver.get('http://127.0.0.1:8000/account/loginPage/') 
        time.sleep(1)
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/input[2]')
        elem.send_keys(user)
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/input[3]')
        elem.send_keys(pwd)
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/div[1]/div/p/button').click()
        time.sleep(1)
        # Code to open Mission Area Report
        driver.get('http://127.0.0.1:8000/projectInfo/')
        time.sleep(1)
        # Click on College Name Data definition
        driver.find_element_by_css_selector('#filters-form > div:nth-child(3) > label > span > i').click()
        time.sleep(2)
        # Open Admin Panel
        driver.get('http://127.0.0.1:8000/admin/')
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="content-main"]/div[2]/table/tbody/tr[3]/th/a').click()
        time.sleep(1)
        driver.get('http://127.0.0.1:8000/admin/home/datadefinition/43/change/')
        # Edit the Data description of College Name
        elem = driver.find_element_by_id("id_description")
        elem.clear()
        time.sleep(2)
        elem.send_keys('Colleges associated to the Campus Partners within UNO Edited by Test Script')
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="datadefinition_form"]/div/div/input[1]').click()
        # Open Mission Area Report to check the changes
        driver.get('http://127.0.0.1:8000/projectInfo/')
        time.sleep(1)
        driver.find_element_by_css_selector('#filters-form > div:nth-child(3) > label > span > i').click()
        time.sleep(5)


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
