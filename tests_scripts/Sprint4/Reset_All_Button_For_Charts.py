from tests_scripts import *
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import os


class ResetAllForCharts(unittest.TestCase):
    # def setUp(self):
    #     self.driver = webdriver.Chrome()

    def test_website(self):
        pathname = os.path.join(os.getcwd(), "chromedriver")
        driver = webdriver.Chrome(pathname)
        self.email = community_partner_user
        self.password = community_partner_pwd

        driver.maximize_window()

        driver.get(sta_url + 'missionchart/')


        self.assertEqual(driver.current_url, sta_url+"missionchart/")

        # Select Mission Areas
        # driver.find_element_by_xpath("(//A[@class='dropdown-item'][text()='Engagement Types']"
        #                              "[text()='Engagement Types'])[2]/preceding-sibling::A").click()

        select = Select(driver.find_element_by_id('id_engagement_type'))
        select.select_by_index(3)
        time.sleep(2)
        select = Select(driver.find_element_by_id('id_academicyear'))
        select.select_by_index(2)
        time.sleep(2)
        select = Select(driver.find_element_by_id('id_campus_partner'))
        select.select_by_index(3)
        time.sleep(2)
        select = Select(driver.find_element_by_id('id_weitz_cec_part'))
        select.select_by_index(2)
        time.sleep(2)

        self.assertNotEqual(sta_url+'missionchart/', driver.current_url)

        # Reset All button
        driver.find_element_by_xpath("//INPUT[@id='btn']/following-sibling::INPUT").click()
        self.assertEqual(sta_url + 'missionchart/', driver.current_url)

        # Validating Engagement Type Chart Reset All button
        driver.get(sta_url + 'engagementtypechart2/')

        self.assertEqual(sta_url + 'engagementtypechart2/', driver.current_url)

        select = Select(driver.find_element_by_id('id_mission'))
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

        self.assertNotEqual(sta_url + 'engagementtypechart2/', driver.current_url)

        # Reset All button
        driver.find_element_by_xpath("//INPUT[@id='btn']/following-sibling::INPUT").click()
        self.assertEqual(sta_url + 'engagementtypechart2/', driver.current_url)

        time.sleep(3)
