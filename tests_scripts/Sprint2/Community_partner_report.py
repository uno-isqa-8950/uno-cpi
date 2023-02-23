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
        driver.get("http://127.0.0.1:8000/account/loginPage/")
        time.sleep(3)
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[2]")
        elem.send_keys(user)
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[3]")
        elem.send_keys(pwd)
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/div[1]/div/p/button').click()
        time.sleep(1)
        elem = driver.find_element_by_xpath('//*[@id="target"]/ul/li[2]/a').click()
        time.sleep(1)
        elem = driver.find_element_by_xpath('//*[@id="target"]/ul/li[2]/ul/li[1]/a')
        time.sleep(1)
        elem = driver.find_element_by_xpath('//*[@id="target"]/ul/li[2]/ul/li[1]/a').click()
        time.sleep(1)
        driver.get('http://127.0.0.1:8000/communitypublicreport/') #Shows Community Partner Report
        time.sleep(1)
        #driver.get('http://127.0.0.1:8000/projectsprivatereport/') #Shows Project Report
        #time.sleep(2)


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
