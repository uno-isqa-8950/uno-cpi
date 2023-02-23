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
        user = "pallavichauhan990@unomaha.edu"
        pwd = "1p2p3p4p5p7#"
        driver = self.driver
        driver.maximize_window()
        driver.get('http://127.0.0.1:8000/account/loginPage/') #Shows Project Report when NOT logged in
        time.sleep(1)
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/input[2]')
        elem.send_keys(user)
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/input[3]')
        elem.send_keys(pwd)
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/div[1]/div/p/button').click()
        time.sleep(1)
        driver.get('http://127.0.0.1:8000/myProjects/')
        time.sleep(1)
        elem = driver.find_element_by_css_selector('#example > thead > tr > th.sorting_asc > span > i').click()
        time.sleep(2)
        driver.get('http://127.0.0.1:8000/projectInfo/')
        time.sleep(1)
        elem = driver.find_element_by_css_selector('#filters-form > div:nth-child(1) > label > span > i').click()
        time.sleep(2)
        driver.get('http://127.0.0.1:8000/engageType/')
        time.sleep(1)
        elem = driver.find_element_by_css_selector('#filters-form > div:nth-child(1) > label > span > i').click()
        time.sleep(2)
        driver.get('http://127.0.0.1:8000/communitypublicreport/')
        time.sleep(1)
        elem = driver.find_element_by_css_selector('#filters-form > div.col-lg-3.col-md-5.form-group.embed-responsive > label > span > i').click()
        time.sleep(2)


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
