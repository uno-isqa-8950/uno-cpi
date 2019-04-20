from tests_scripts import *
import unittest
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import os


class ProjectDuplicateValidation(unittest.TestCase):
    def setUp(self):
        pathname = os.path.join(os.getcwd(), "chromedriver")
        self.driver = webdriver.Chrome(pathname)

    def test_create_project(self):
        driver = self.driver
        # self.email = community_partner_user
        # self.password = community_partner_pwd
        thankyou = "Your project has been successfully added. " \
                   "A campus partner user can edit an associated project at any time from the My Projects page."
        driver.maximize_window()

        driver.get(sta_url+'login/')
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys(campus_partner_user)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(campus_partner_pwd)
        driver.find_element_by_name("password").send_keys(Keys.ENTER)

        driver.get(sta_url+"createProject/")
        driver.find_element_by_id("id_project_name").click()
        driver.find_element_by_id("id_project_name").clear()
        driver.find_element_by_id("id_project_name").send_keys("EdemTest2020")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Select Engagement Type'])[1]/following::span[1]").click()
        driver.find_element_by_id("select2-id_activity_type-container").click()

        Select(driver.find_element_by_id("id_engagement_type")).select_by_visible_text("Volunteering")
        Select(driver.find_element_by_id("id_activity_type")).select_by_visible_text("Unpaid Services")

        driver.find_element_by_id("id_community-0-community_partner").click()
        Select(driver.find_element_by_id("id_community-0-community_partner")).select_by_visible_text(
            "Greater Birmingham Humane Society")
        driver.find_element_by_id("id_community-0-community_partner").click()
        driver.find_element_by_id("id_campus-0-campus_partner").click()
        Select(driver.find_element_by_id("id_campus-0-campus_partner")).select_by_visible_text(
            "Thompson Learning Community")
        driver.find_element_by_id("id_campus-0-campus_partner").click()
        driver.find_element_by_id("id_mission-0-mission").click()
        Select(driver.find_element_by_id("id_mission-0-mission")).select_by_visible_text("Educational Support")
        driver.find_element_by_id("id_mission-0-mission").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Select Semester'])[1]/following::span[1]").click()
        Select(driver.find_element_by_id("id_semester")).select_by_visible_text("Fall")

        driver.find_element_by_id("id_total_uno_students").click()
        driver.find_element_by_id("id_total_uno_students").clear()
        driver.find_element_by_id("id_total_uno_students").send_keys(10)
        driver.find_element_by_id("id_total_uno_hours").click()
        driver.find_element_by_id("id_total_uno_hours").clear()
        driver.find_element_by_id("id_total_uno_hours").send_keys(10)
        driver.find_element_by_id("id_address_line1").click()
        driver.find_element_by_id("id_address_line1").clear()
        driver.find_element_by_id("id_address_line1").send_keys("8509 Maple Ct")
        driver.find_element_by_id("id_city").clear()
        driver.find_element_by_id("id_city").send_keys("Lavista")
        driver.find_element_by_id("id_state").clear()
        driver.find_element_by_id("id_state").send_keys("NE")
        driver.find_element_by_id("id_zip").clear()
        driver.find_element_by_id("id_zip").send_keys("68128")
        driver.find_element_by_id("id_country").clear()
        driver.find_element_by_id("id_country").send_keys("USA")
        driver.find_element_by_xpath('//*[@id="terms"]').click()
        time.sleep(5)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Country'])[1]/following::button[1]").click()
        # time.sleep(30)


    def tearDown(self):
        self.driver.close()
        self.driver.stop_client()


if __name__ == "__main__":
    unittest.main()
