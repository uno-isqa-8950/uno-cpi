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
        user = "" # (Put user email here)
        pwd = "" #(Put password here)
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/login/")
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='target']/ul/li[4]/a").click()
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[2]")
        elem.send_keys(user)
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[3]")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        assert "Logged In"
        time.sleep(3)

        # elem = driver.find_element_by_xpath("//*[@id='target']/ul/li[2]/a").click()
        # time.sleep(3)
        # elem = driver.find_element_by_xpath("//*[@id='target']/ul/li[2]/ul/li[1]/a").click()
        # time.sleep(3)
        # elem = driver.find_element_by_xpath("//*[@id='target']/ul/li[2]/ul/li[1]/ul/a[3]").click()
        # time.sleep(3)
        driver.get("http://127.0.0.1:8000/communitypublicreport/")
        time.sleep(1)
        # elem = driver.find_element_by_xpath('//*[@id="select2-id_academic_year-container"]').click()
        # time.sleep(3)
        #driver.find_element_by_link_text("Analytics").click()
        driver.get("http://127.0.0.1:8000/communitypublicreport/?academic_year=1&mission=All&weitz_cec_part=All&community_type=")
        time.sleep(1)
        driver.get("http://127.0.0.1:8000/communitypublicreport/?academic_year=1&mission=1&weitz_cec_part=All&community_type=")
        time.sleep(1)
        driver.get("http://127.0.0.1:8000/communitypublicreport/?academic_year=1&mission=1&weitz_cec_part=Yes&community_type=")
        time.sleep(1)
        driver.get("http://127.0.0.1:8000/communitypublicreport/?academic_year=1&mission=1&weitz_cec_part=Yes&community_type=1")
        time.sleep(3)



    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
