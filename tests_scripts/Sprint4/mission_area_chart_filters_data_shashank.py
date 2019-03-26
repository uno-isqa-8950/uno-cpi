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
        # Opens mission area chart
        driver.get('http://127.0.0.1:8000/missionchart/')
        time.sleep(1)
        # Applies engagement type filter
        driver.find_element_by_xpath('//*[@id="id_engagement_type"]/option[3]').click()
        time.sleep(5)
        # Applies academic year filter
        driver.find_element_by_xpath('//*[@id="id_academicyear"]/option[4]').click()
        time.sleep(5)
        # Resets all the filters
        driver.get('http://127.0.0.1:8000/missionchart/')
        time.sleep(1)
        # Applies multiple filters
        driver.find_element_by_xpath('//*[@id="id_college_name"]/option[5]').click()
        driver.find_element_by_xpath('//*[@id="id_weitz_cec_part"]/option[3]').click()
        driver.find_element_by_xpath('//*[@id="id_community_type"]/option[6]').click()
        time.sleep(5)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()