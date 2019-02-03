import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os


class SimpleLoginLogout(unittest.TestCase):
    pathname = os.path.join(os.getcwd(), "chromedriver")
    driver = webdriver.Chrome(pathname)


    def setUp(self):

        self.driver = webdriver.Chrome()
        self.base_url = "https://uno-cpi-cat.herokuapp.com"
        self.test_url = "127.0.0.1:8000"
        self.email = "aanzalone@unomaha.edu"
        self.password = "Capstone2019"

    def test_Register(self):
        driver = self.driver
        base_url = self.base_url
        # test_url = self.test_url

        driver.maximize_window()

        """
        Change between base_url(APP) and test_url(LOCAL) if testing locally or the app
        """
        driver.get(base_url)
        time.sleep(2)