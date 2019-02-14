import unittest
import time
from selenium import webdriver
import os
from tests_scripts import *


class UrlRedirect(unittest.TestCase):
    pathname = os.path.join(os.getcwd(), "chromedriver")
    driver = webdriver.Chrome(pathname)

    def setUp(self):

        self.driver = webdriver.Chrome()
        self.base_url = base_url

    def test_Url_Redirect(self):
        driver = self.driver
        base_url = self.base_url
        driver.maximize_window()

        driver.get(base_url)
        time.sleep(2)
        assert "https://uno-cpi-cat.herokuapp.com" in driver.current_url
        time.sleep(2)

    def tearDown(self):
        self.driver.close()
        self.driver.stop_client()

if __name__ == "__main__":
    unittest.main()
