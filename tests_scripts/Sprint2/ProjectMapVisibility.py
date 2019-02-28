import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class projectMapVisibility(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.url = "http://127.0.0.1:8000/home"

    def test_campusPartnerUser(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(self.url)
        time.sleep(2)

        driver.find_element_by_xpath("//*[@id='target']/ul/li[4]/a").click()
        elem = driver.find_element_by_xpath("//input[@name='email']")
        elem.send_keys("campuspartner@unomaha.edu")
        elem = driver.find_element_by_xpath("//input[@name='password']")
        elem.send_keys("Capstone2019!")
        elem.send_keys(Keys.RETURN)
        assert "Logged In"
        time.sleep(2)

        #Open Project map
        driver.find_element_by_xpath("//div[@id='target']/ul/li/a").click()
        driver.find_element_by_xpath("//div[@id='target']/ul/li/div/a[4]").click()
        assert "Campus User Passed"

    def test_adminUser(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(self.url)
        time.sleep(2)

        driver.find_element_by_xpath("//*[@id='target']/ul/li[4]/a").click()
        elem = driver.find_element_by_xpath("//input[@name='email']")
        elem.send_keys("adminuser@unomaha.edu")
        elem = driver.find_element_by_xpath("//input[@name='password']")
        elem.send_keys("Capstone2019!")
        elem.send_keys(Keys.RETURN)
        assert "Logged In"
        time.sleep(2)

        #Open Project map
        driver.find_element_by_xpath("//div[@id='target']/ul/li/a").click()
        driver.find_element_by_xpath("//div[@id='target']/ul/li/div/a[4]").click()
        assert "Admin User Passed"

    def test_publicUser(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(self.url)
        time.sleep(2)

        #Open Project map
        driver.find_element_by_xpath("//div[@id='target']/ul/li/a").click()
        driver.find_element_by_xpath("//div[@id='target']/ul/li/div/a[4]").click()
        assert "Public User Passed"

    def tearDown(self):
        self.driver.close()
        self.driver.stop_client()

if __name__ == "__main__":
    unittest.main()
