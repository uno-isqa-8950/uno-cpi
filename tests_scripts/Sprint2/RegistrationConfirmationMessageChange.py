from tests_scripts import *
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import os


class RegistrationConfirmationMessage(unittest.TestCase):


    def test_Community_Partner_Registration_Confirmation(self):
        pathname = os.path.join(os.getcwd(), "chromedriver")
        driver = webdriver.Chrome(pathname)

        driver.maximize_window()

        driver.get(test_url)
        driver.find_element_by_link_text("Register").click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Campus Partner'])[1]/following::a[1]").click()

        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("Viz29")
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
        time.sleep(8)
        self.assertEqual(driver.find_element_by_xpath("/html/body/div/div/div/div[2]/p").text,"Your organization is successfully registered as a UNO community partner")

    def test_Campus_Partner_Registration_Confirmation(self):
        pathname = os.path.join(os.getcwd(), "chromedriver")
        driver = webdriver.Chrome(pathname)

        driver.get(test_url)
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/a").click()
        driver.find_element_by_xpath("/html/body/nav/div/ul/li[3]/div/a[1]").click()
        self.assertEqual(test_url+"partners/registerCampusPartner/",driver.current_url )
        time.sleep(1)
        elem = driver.find_element_by_xpath("//*[@id='id_name']")
        elem.send_keys("Vix201")  #After every test, put a different name here
        time.sleep(1)
        select = Select(driver.find_element_by_id('id_college_name'))
        select.select_by_index(1)
        select = Select(driver.find_element_by_id('id_form-0-contact_type'))
        select.select_by_index(2)
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-email_id"]')
        elem.send_keys(campus_partner_user)
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-first_name"]')
        elem.send_keys('Edward')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-last_name"]')
        elem.send_keys('Jones')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-work_phone"]')
        elem.send_keys('1234567890')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-cell_phone"]')
        elem.send_keys('0987654321')
        #Submit button
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/form/div/div/div[5]/div/button').click()
        self.assertEqual(driver.find_element_by_xpath("/html/body/div/div/div/div[2]/p").text,
                         "Your organization is successfully registered as a campus partner")

