import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class UnoCpiTest(unittest.TestCase):
    driver = webdriver.Chrome('C:/CAPSTONE/seleniumtests/uno-cpi_test/Selenium drivers/chromedriver')  # Optional argument, if not specified will search path.

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://uno-cpi.herokuapp.com"

    def test_register_and_login_to_u_n_o_c_p_i(self):
        driver = self.driver
        base_url = self.base_url

        driver.maximize_window()
        driver.get(base_url)
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_link_text("Campus Partner User Signup").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Select a Campus Partner'])[1]/following::span[1]").click()
        driver.find_element_by_id("id_first_name").clear()
        driver.find_element_by_id("id_first_name").send_keys("Edem")
        driver.find_element_by_id("id_last_name").clear()
        driver.find_element_by_id("id_last_name").send_keys("Dosseh")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("edosseh@unomaha.edu")
        driver.find_element_by_id("id_password").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("fro$ty04")
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("fro$ty04")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Confirm Password'])[1]/following::button[1]").click()

    def tearDown(self):
        self.driver.close()
        self.driver.stop_client()

    if __name__ == "__main__":
        unittest.main()