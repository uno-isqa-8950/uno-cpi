import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

class projectAssociated(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_website(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/")

        driver.get('http://127.0.0.1:8000/projectInfo/')
        select = Select(driver.find_element_by_id('id_engagement_type'))
        select.select_by_index(3)
        time.sleep(2)
        select = Select(driver.find_element_by_id('id_academic_year'))
        select.select_by_index(2)
        time.sleep(2)
        select = Select(driver.find_element_by_id('id_campus_partner'))
        select.select_by_index(3)
        time.sleep(2)
        select = Select(driver.find_element_by_id('id_weitz_cec_part'))
        select.select_by_index(2)
        time.sleep(2)
        elem=driver.find_element_by_xpath('//*[@id="btn"]').click()
        time.sleep(3)