from tests_scripts import *
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os


class UpdatedProjectFormValidation(unittest.TestCase):

    def test_project_creation_prompt(self):
        pathname = os.path.join(os.getcwd(), "chromedriver")
        driver = webdriver.Chrome(pathname)

        driver.maximize_window()

        # 1. Login as a campus partner user
        driver.get(test_url)
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys(campus_partner_user)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(campus_partner_pwd)
        driver.find_element_by_name("password").send_keys(Keys.ENTER)

        # Click on Projects button
        driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/a").click()
        # Click on Create Project button
        driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/div/a[3]").click()

        # 2. Create new campus and community partners from the project form

        # Create campus partner
        # driver.find_element_by_xpath(
        #     "//A[@class='btn btn-link'][text()='Register a New Community Partner']/preceding-sibling::A").click()
        # driver.switch_to.alert.accept()
        # self.assertEqual("http://127.0.0.1:8000/partners/registerCampusPartnerForProject/", driver.current_url)
        #
        # elem = driver.find_element_by_xpath("//*[@id='id_name']")
        # # After every test, put a different name here
        # elem.send_keys("XYZ Corp 5")
        # time.sleep(1)
        # select = Select(driver.find_element_by_id('id_college_name'))
        # select.select_by_index(1)
        # select = Select(driver.find_element_by_id('id_form-0-contact_type'))
        # select.select_by_index(2)
        # elem = driver.find_element_by_xpath('//*[@id="id_form-0-email_id"]')
        # elem.send_keys(campus_partner_user)
        # elem = driver.find_element_by_xpath('//*[@id="id_form-0-first_name"]')
        # elem.send_keys('Edward')
        # elem = driver.find_element_by_xpath('//*[@id="id_form-0-last_name"]')
        # elem.send_keys('Jones')
        # elem = driver.find_element_by_xpath('//*[@id="id_form-0-work_phone"]')
        # elem.send_keys('1234567890')
        # elem = driver.find_element_by_xpath('//*[@id="id_form-0-cell_phone"]')
        # elem.send_keys('0987654321')
        # # Submit button
        # driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/form/div/div/div[5]/div/button').click()
        # # Validate redirect back to Project Form
        # self.assertEqual("http://127.0.0.1:8000/project_total_Add/", driver.current_url)

        # Create community partner
        # driver.find_element_by_xpath(
        #     "//A[@class='btn btn-link'][text()='Register a New Campus Partner']/following-sibling::A").click()
        # driver.switch_to.alert.accept()
        # self.assertEqual("http://127.0.0.1:8000/partners/registerCommunityPartnerForProject/", driver.current_url)
        #
        # driver.find_element_by_id("id_name").clear()
        # # After every test, put a different name here
        # driver.find_element_by_id("id_name").send_keys("XYZ Corp 5")
        # driver.find_element_by_id("id_website_url").clear()
        # driver.find_element_by_id("id_website_url").send_keys("https://www.xyzcorpcanada.com")
        #
        # driver.find_element_by_xpath("//select[@name='community_type']/option[text()='Nonprofit']").click()
        # driver.find_element_by_id("id_address_line1").click()
        # driver.find_element_by_id("id_address_line1").clear()
        # driver.find_element_by_id("id_address_line1").send_keys("8509 Maple Ct")
        # driver.find_element_by_id("id_city").clear()
        # driver.find_element_by_id("id_city").send_keys("Omaha")
        # driver.find_element_by_id("id_state").clear()
        # driver.find_element_by_id("id_state").send_keys("NE")
        # driver.find_element_by_id("id_zip").clear()
        # driver.find_element_by_id("id_zip").send_keys("68128")
        # driver.find_element_by_id("id_country").clear()
        # driver.find_element_by_id("id_country").send_keys("USA")
        # driver.find_element_by_id("id_contact-0-email_id").click()
        # driver.find_element_by_id("id_contact-0-email_id").clear()
        # driver.find_element_by_id("id_contact-0-email_id").send_keys("jamesdean@gmail.com")
        # driver.find_element_by_id("id_contact-0-first_name").clear()
        # driver.find_element_by_id("id_contact-0-first_name").send_keys("Jean")
        # driver.find_element_by_id("id_contact-0-last_name").clear()
        # driver.find_element_by_id("id_contact-0-last_name").send_keys("Dean")
        # driver.find_element_by_id("id_contact-0-work_phone").clear()
        # driver.find_element_by_id("id_contact-0-work_phone").send_keys("4021111111")
        # driver.find_element_by_id("id_mission-0-mission_area").click()
        # Select(driver.find_element_by_id("id_mission-0-mission_area")).select_by_visible_text("Educational Support")
        # driver.find_element_by_xpath(
        #     "(.//*[normalize-space(text()) and normalize-space(.)='Mission Area'])[3]/following::option[2]").click()
        # driver.find_element_by_xpath(
        #     "(.//*[normalize-space(text()) and normalize-space(.)='Mission Area'])[3]/following::button[1]").click()
        # driver.find_element_by_id("id_mission-1-mission_type").click()
        # Select(driver.find_element_by_id("id_mission-1-mission_type")).select_by_visible_text("Other")
        # driver.find_element_by_xpath(
        #     "(.//*[normalize-space(text()) and normalize-space(.)='Mission Type'])[2]/following::option[2]").click()
        # driver.find_element_by_id("id_mission-1-mission_area").click()
        # Select(driver.find_element_by_id("id_mission-1-mission_area")).select_by_visible_text("Health and Wellness")
        #
        # # Submit button
        # driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div[2]/form/div[5]/div/button").click()
        # # Validate redirect back to Project Form
        # self.assertEqual("http://127.0.0.1:8000/project_total_Add/", driver.current_url)

        # Fill project form  with new campus and community partners information and international address
        elem = driver.find_element_by_id("id_project_name")
        # After every test, put a different name here
        elem.send_keys("Canada Project 11")
        # for Engagement type
        driver.find_element_by_xpath('//*[@id="id_engagement_type"]/option[2]').click()
        # for Activity Type
        driver.find_element_by_xpath('//*[@id="id_activity_type"]/option[3]').click()

        # for Campus Partner Information
        elem = driver.find_element_by_xpath(
            "//BUTTON[@class='btn btn-secondary add-campus-row'][text()='Add an Additional Campus Partner']"
            "/../..//SELECT[@id='id_campus-0-campus_partner']")
        elem.click()
        Select(elem).select_by_visible_text("XYZ Corp 5")

        # for Campus Partner Information
        elem = driver.find_element_by_xpath(
            "//BUTTON[@class='btn btn-secondary add-community-row'][text()='Add an Additional Community Partner']"
            "/../..//SELECT[@id='id_community-0-community_partner']")
        elem.click()
        Select(elem).select_by_visible_text("XYZ Corp 5")

        # for Project Mission Area
        # Mission Type
        # elem = driver.find_element_by_name("mission-0-mission_type")
        # elem.click()
        # Select(elem).select_by_visible_text("Primary")
        # Mission Area
        elem = driver.find_element_by_name("mission-0-mission")
        elem.click()
        Select(elem).select_by_visible_text("Social Justice")

        # for Status
        driver.find_element_by_xpath('//*[@id="id_status"]/option[2]').click()
        # For semester
        elem = driver.find_element_by_id("id_semester")
        elem.send_keys("Spring")
        # for academic year
        driver.find_element_by_xpath('//*[@id="id_academic_year"]/option[3]').click()
        # for address/ international address
        elem = driver.find_element_by_id("id_address_line1")
        elem.send_keys("10-123 1/2 Main Street NW")
        elem = driver.find_element_by_id("id_city")
        elem.send_keys("Montreal")
        elem = driver.find_element_by_id("id_state")
        elem.send_keys("QC1")
        elem = driver.find_element_by_id("id_zip")
        elem.send_keys("H3Z 2Y7")
        elem = driver.find_element_by_id("id_country")
        elem.send_keys("Canada")

        # Submit button
        driver.find_element_by_xpath("//INPUT[@id='id_country']/../../../../../../..//"
                                     "BUTTON[@type='submit'][text()='Submit']").click()
        time.sleep(10)
        self.assertEqual(driver.find_element_by_xpath("/html/body/div/div/div/div[2]/p").text,
                         "Your project has been successfully added")


if __name__ == "__main__":
    unittest.main()
