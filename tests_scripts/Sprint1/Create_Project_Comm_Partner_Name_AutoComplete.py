import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
from tests_scripts import *



class CommunityPartnerAutoComplete(unittest.TestCase):
    pathname = os.path.join(os.getcwd(), "chromedriver")
    driver = webdriver.Chrome(pathname)

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.url = url

    def test_CommunityPartnerAutoComplete(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(self.url)


        driver.find_element_by_xpath("//*[@id='target']/ul/li[4]/a").click()
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[2]")
        elem.send_keys(campus_partner_user )
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[3]")
        elem.send_keys(campus_partner_pwd)
        elem.send_keys(Keys.RETURN)
        assert "Logged In"

        # xpath, clicks on project button
        driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/a").click()
        # clicks on create project button
        driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/div/a[3]").click()
        elem = driver.find_element_by_id("id_project_name")
        elem.send_keys("Lecture on Human Rights")
        # for Engagement type
        driver.find_element_by_xpath('//*[@id="id_engagement_type"]/option[6]').click()
        # for Activity Type
        driver.find_element_by_xpath('//*[@id="id_activity_type"]/option[5]').click()

        # Sending part of the Community Partner Names returns/suggests matching partner's name
        driver.find_element_by_id("id_campus-0-campus_partner").send_keys("Medi")
        time.sleep(5)
        driver.find_element_by_id("id_campus-0-campus_partner").send_keys("Nativ")
        time.sleep(5)
        driver.find_element_by_id("id_campus-0-campus_partner").send_keys("Phil")
        time.sleep(5)
        driver.find_element_by_id("id_campus-0-campus_partner").send_keys("Chine")
        time.sleep(5)

        # mySelect = Select(driver.find_element_by_id("id_campus-0-campus_partner"))
        # mySelect.select_by_visible_text("Common Reader")
        # time.sleep(10)
        # mySelect.select_by_visible_text("Management")
        # time.sleep(10)
        # mySelect.select_by_visible_text("Journalism")
        # time.sleep(10)
