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

    def test_Login(self):
        driver = self.driver
        base_url = self.base_url
        # test_url = self.test_url

        driver.maximize_window()

        """
        Change between base_url(APP) and test_url(LOCAL) if testing locally or the app
        """
        driver.get(base_url)
        time.sleep(2)
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys(self.email)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(self.password)
        #driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Password'])[1]/following::button[1]").click()
        #driver.find_element_by_xpath("//a[contains(@href, '/account/loginPage/')]").click()
        driver.find_element_by_name("password").send_keys(Keys.ENTER)
        self.assertNotEqual("https://uno-cpi-cat.herokuapp.com/account/loginPage/",driver.current_url )


    def test_Logout(self):

        driver = self.driver
        base_url = self.base_url
        # test_url = self.test_url

        driver.maximize_window()

        """
        Change between base_url(APP) and test_url(LOCAL) if testing locally or the app
        """
        driver.get(base_url)
        time.sleep(2)
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys(self.email)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(self.password)
        #driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Password'])[1]/following::button[1]").click()
        #driver.find_element_by_xpath("//a[contains(@href, '/account/loginPage/')]").click()
        driver.find_element_by_name("password").send_keys(Keys.ENTER)
        self.assertNotEqual("https://uno-cpi-cat.herokuapp.com/account/loginPage/", driver.current_url)
        #driver.find_element_by_link_text("Edem").click()
        driver.find_element_by_xpath("(//a[contains(@href, '#')])[6]").click()
        #driver.find_element_by_link_text("Logout").click()
        driver.find_element_by_xpath("//a[contains(@href, '/logout/')]").click() # Logout
        assert "https://uno-cpi-cat.herokuapp.com/logout/" in driver.current_url

    def tearDown(self):
        self.driver.close()
        self.driver.stop_client()

if __name__ == "__main__":
    unittest.main()