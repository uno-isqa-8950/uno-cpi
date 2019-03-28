from tests_scripts import *
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import os


class HiddenDefaultFilters(unittest.TestCase):
    def setUp(self):
        pathname = os.path.join(os.getcwd(), "chromedriver")
        self.driver = webdriver.Chrome(pathname)

    def test_hidden_filters_not_logged_in(self):
        driver = self.driver
        # self.email = community_partner_user
        # self.password = community_partner_pwd

        driver.maximize_window()

        # REPORTS
        driver.get(sta_url + 'projectInfo/')
        self.assertFalse(driver.find_element_by_id('id_academic_year').is_displayed())

        driver.get(sta_url + 'engageType/')
        self.assertFalse(driver.find_element_by_id('id_academic_year').is_displayed())

        driver.get(sta_url + 'communitypublicreport/')
        self.assertFalse(driver.find_element_by_id('id_academic_year').is_displayed())

        driver.get(sta_url + 'projectspublicreport/')
        self.assertFalse(driver.find_element_by_id('id_academic_year').is_displayed())

        # CHARTS
        driver.get(sta_url + 'missionchart/')
        self.assertFalse(driver.find_element_by_id('id_academicyear').is_displayed())

        driver.get(sta_url + 'engagementtypechart2/')
        self.assertFalse(driver.find_element_by_id('id_academic_year').is_displayed())

    # def test_filters_remain_opened_when_selected_not_logged_in(self):
    #     driver = self.driver
    #     # self.email = community_partner_user
    #     # self.password = community_partner_pwd
    #
    #     driver.maximize_window()
    #
    #     # REPORTS
    #     driver.get(sta_url + 'projectInfo/')
    #     driver.find_element_by_xpath("//INPUT[@id='btn']/preceding-sibling::INPUT").click()
    #     select = Select(driver.find_element_by_id('id_academic_year'))
    #     select.select_by_index(2)
    #     self.assertTrue(driver.find_element_by_id('id_academic_year').is_displayed())
    #
    #     driver.get(sta_url + 'engageType/')
    #     driver.find_element_by_xpath("//INPUT[@id='btn']/preceding-sibling::INPUT").click()
    #     select = Select(driver.find_element_by_id('id_academic_year'))
    #     select.select_by_index(2)
    #     self.assertTrue(driver.find_element_by_id('id_academic_year').is_displayed())
    #
    #     driver.get(sta_url + 'communitypublicreport/')
    #     driver.find_element_by_xpath("//INPUT[@id='btn']/preceding-sibling::INPUT").click()
    #     select = Select(driver.find_element_by_id('id_academic_year'))
    #     select.select_by_index(2)
    #     self.assertTrue(driver.find_element_by_id('id_academic_year').is_displayed())
    #
    #     driver.get(sta_url + 'projectspublicreport/')
    #     driver.find_element_by_xpath("//INPUT[@id='btn']/preceding-sibling::INPUT").click()
    #     select = Select(driver.find_element_by_id('id_academic_year'))
    #     select.select_by_index(2)
    #     self.assertTrue(driver.find_element_by_id('id_academic_year').is_displayed())
    #
    #     # CHARTS
    #     driver.get(sta_url + 'missionchart/')
    #     driver.find_element_by_xpath("//INPUT[@id='btn']/preceding-sibling::INPUT").click()
    #     select = Select(driver.find_element_by_id('id_academicyear'))
    #     select.select_by_index(2)
    #     self.assertTrue(driver.find_element_by_id('id_academicyear').is_displayed())
    #
    #     driver.get(sta_url + 'engagementtypechart2/')
    #     driver.find_element_by_xpath("//INPUT[@id='btn']/preceding-sibling::INPUT").click()
    #     select = Select(driver.find_element_by_id('id_academic_year'))
    #     select.select_by_index(2)
    #     self.assertTrue(driver.find_element_by_id('id_academic_year').is_displayed())

    def test_hidden_filters_logged_in(self):
        driver = self.driver
        self.email = community_partner_user
        self.password = community_partner_pwd

        driver.get(sta_url)
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys(self.email)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(self.password)
        driver.find_element_by_name("password").send_keys(Keys.ENTER)

        driver.maximize_window()

        # REPORTS
        driver.get(sta_url + 'projectInfo/')
        self.assertFalse(driver.find_element_by_id('id_academic_year').is_displayed())

        driver.get(sta_url + 'engageType/')
        self.assertFalse(driver.find_element_by_id('id_academic_year').is_displayed())

        driver.get(sta_url + 'communitypublicreport/')
        self.assertFalse(driver.find_element_by_id('id_academic_year').is_displayed())

        driver.get(sta_url + 'projectspublicreport/')
        self.assertFalse(driver.find_element_by_id('id_academic_year').is_displayed())

        # CHARTS
        driver.get(sta_url + 'missionchart/')
        self.assertFalse(driver.find_element_by_id('id_academicyear').is_displayed())

        driver.get(sta_url + 'engagementtypechart2/')
        self.assertFalse(driver.find_element_by_id('id_academic_year').is_displayed())

    # def test_filters_remain_opened_when_selected_logged_in(self):
    #     driver = self.driver
    #     self.email = community_partner_user
    #     self.password = community_partner_pwd
    #
    #     driver.get(sta_url)
    #     driver.find_element_by_link_text("Login").click()
    #     driver.find_element_by_name("email").click()
    #     driver.find_element_by_name("email").clear()
    #     driver.find_element_by_name("email").send_keys(self.email)
    #     driver.find_element_by_name("password").clear()
    #     driver.find_element_by_name("password").send_keys(self.password)
    #     driver.find_element_by_name("password").send_keys(Keys.ENTER)
    #
    #     driver.maximize_window()
    #
    #     # REPORTS
    #     driver.get(sta_url + 'projectInfo/')
    #     driver.find_element_by_xpath("//INPUT[@id='btn']/preceding-sibling::INPUT").click()
    #     select = Select(driver.find_element_by_id('id_academic_year'))
    #     select.select_by_index(2)
    #     self.assertTrue(driver.find_element_by_id('id_academic_year').is_displayed())
    #
    #     driver.get(sta_url + 'engageType/')
    #     driver.find_element_by_xpath("//INPUT[@id='btn']/preceding-sibling::INPUT").click()
    #     select = Select(driver.find_element_by_id('id_academic_year'))
    #     select.select_by_index(2)
    #     self.assertTrue(driver.find_element_by_id('id_academic_year').is_displayed())
    #
    #     driver.get(sta_url + 'communitypublicreport/')
    #     driver.find_element_by_xpath("//INPUT[@id='btn']/preceding-sibling::INPUT").click()
    #     select = Select(driver.find_element_by_id('id_academic_year'))
    #     select.select_by_index(2)
    #     self.assertTrue(driver.find_element_by_id('id_academic_year').is_displayed())
    #
    #     driver.get(sta_url + 'projectspublicreport/')
    #     driver.find_element_by_xpath("//INPUT[@id='btn']/preceding-sibling::INPUT").click()
    #     select = Select(driver.find_element_by_id('id_academic_year'))
    #     select.select_by_index(2)
    #     self.assertTrue(driver.find_element_by_id('id_academic_year').is_displayed())
    #
    #     # CHARTS
    #     driver.get(sta_url + 'missionchart/')
    #     driver.find_element_by_xpath("//INPUT[@id='btn']/preceding-sibling::INPUT").click()
    #     select = Select(driver.find_element_by_id('id_academicyear'))
    #     select.select_by_index(2)
    #     self.assertTrue(driver.find_element_by_id('id_academicyear').is_displayed())
    #
    #     driver.get(sta_url + 'engagementtypechart2/')
    #     driver.find_element_by_xpath("//INPUT[@id='btn']/preceding-sibling::INPUT").click()
    #     select = Select(driver.find_element_by_id('id_academic_year'))
    #     select.select_by_index(2)
    #     self.assertTrue(driver.find_element_by_id('id_academic_year').is_displayed())

    def tearDown(self):
        self.driver.close()
        self.driver.stop_client()


if __name__ == "__main__":
    unittest.main()
