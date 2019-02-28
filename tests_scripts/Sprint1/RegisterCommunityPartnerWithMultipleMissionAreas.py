import unittest
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import os
from tests_scripts import *


class RegisterCommunityPartnerWithMultipleMissionAreas(unittest.TestCase):
    pathname = os.path.join(os.getcwd(), "chromedriver")
    driver = webdriver.Chrome(pathname)

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_register_campus_partner_595(self):
        driver = self.driver

        test_url = url
        driver.maximize_window()

        driver.get(test_url)
        driver.find_element_by_link_text("Register").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Campus Partner'])[1]/following::a[1]").click()
        # /html/body/nav/div/ul/li[3]/div/a[1]
        driver.find_element_by_id("id_name").clear()

        # Validation autocomplete functionality
        driver.find_element_by_id("id_name").send_keys("Jer")
        time.sleep(5)
        driver.find_element_by_id("id_name").clear()

        driver.find_element_by_id("id_name").send_keys("TD")
        time.sleep(5)
        driver.find_element_by_id("id_name").clear()

        driver.find_element_by_id("id_name").send_keys("Van")
        time.sleep(5)
        driver.find_element_by_id("id_name").clear()

        driver.find_element_by_id("id_name").send_keys("VanguardFund100")
        driver.find_element_by_id("id_website_url").clear()
        driver.find_element_by_id("id_website_url").send_keys("https://www.jeandeanfoundation.com")

        driver.find_element_by_xpath("//select[@name='community_type']/option[text()='Nonprofit']").click()
        driver.find_element_by_id("id_address_line1").click()
        driver.find_element_by_id("id_address_line1").clear()
        driver.find_element_by_id("id_address_line1").send_keys("8509 Maple Ct")
        driver.find_element_by_id("id_city").clear()
        driver.find_element_by_id("id_city").send_keys("Omaha")
        driver.find_element_by_id("id_state").clear()
        driver.find_element_by_id("id_state").send_keys("NE")
        driver.find_element_by_id("id_zip").clear()
        driver.find_element_by_id("id_zip").send_keys("68128")
        driver.find_element_by_id("id_country").clear()
        driver.find_element_by_id("id_country").send_keys("USA")
        driver.find_element_by_id("id_contact-0-email_id").click()
        driver.find_element_by_id("id_contact-0-email_id").clear()
        driver.find_element_by_id("id_contact-0-email_id").send_keys("jamesdean@gmail.com")
        driver.find_element_by_id("id_contact-0-first_name").clear()
        driver.find_element_by_id("id_contact-0-first_name").send_keys("Jean")
        driver.find_element_by_id("id_contact-0-last_name").clear()
        driver.find_element_by_id("id_contact-0-last_name").send_keys("Dean")
        driver.find_element_by_id("id_contact-0-work_phone").clear()
        driver.find_element_by_id("id_contact-0-work_phone").send_keys("4021111111")
        driver.find_element_by_id("id_mission-0-mission_area").click()
        Select(driver.find_element_by_id("id_mission-0-mission_area")).select_by_visible_text("Educational Support")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Mission Area'])[3]/following::option[2]").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Mission Area'])[3]/following::button[1]").click()
        driver.find_element_by_id("id_mission-1-mission_type").click()
        Select(driver.find_element_by_id("id_mission-1-mission_type")).select_by_visible_text("Other")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Mission Type'])[2]/following::option[2]").click()
        driver.find_element_by_id("id_mission-1-mission_area").click()
        Select(driver.find_element_by_id("id_mission-1-mission_area")).select_by_visible_text("Health and Wellness")

        # Submit button
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div[2]/form/div[5]/div/button").click()


        # Go check admin page
        driver.get(test_url)

        driver.find_element_by_xpath("//*[@id='target']/ul/li[4]/a").click()
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[2]")
        elem.send_keys(admin_user)
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[3]")
        elem.send_keys(admin_pwd)
        elem.send_keys(Keys.RETURN)
        assert "Logged In"

        driver.get(test_url+"admin/partners/communitypartnermission/")
        time.sleep(15)

    def tearDown(self):
        self.driver.close()
        self.driver.stop_client()

if __name__ == "__main__":
    unittest.main()