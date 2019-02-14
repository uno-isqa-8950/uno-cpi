import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from tests_scripts import *



class ActvtyTypeCoursePromptForCourseInfo(unittest.TestCase):
    pathname = os.path.join(os.getcwd(), "chromedriver")
    driver = webdriver.Chrome(pathname)

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.url = url

    def test_CourseInfoRequired(self):
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
        # for Engagement type (Service Learning no longer prompt for course info)
        driver.find_element_by_xpath('//*[@id="id_engagement_type"]/option[6]').click()
        time.sleep(5)
        # for Activity Type (Picking Course prompt for info details)
        driver.find_element_by_xpath('//*[@id="id_activity_type"]/option[5]').click()
        time.sleep(5)
        # for Status
        driver.find_element_by_xpath('//*[@id="id_status"]/option[2]').click()
        # For semester
        elem = driver.find_element_by_id("id_semester")
        elem.send_keys("Spring")
        # for academic year
        driver.find_element_by_xpath('//*[@id="id_academic_year"]/option[3]').click()
        # for address
        elem = driver.find_element_by_id("id_address_line1")
        elem.send_keys("171 Q st")
        elem = driver.find_element_by_id("id_city")
        elem.send_keys("Omaha")
        elem = driver.find_element_by_id("id_state")
        elem.send_keys("NE")
        elem = driver.find_element_by_id("id_zip")
        elem.send_keys("68135")
        elem = driver.find_element_by_id("id_country")
        elem.send_keys("USA")

        # clicks on submit form button
        # driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/form/div[8]/div/button").click()
        time.sleep(9)

    def tearDown(self):
        self.driver.close()
        self.driver.stop_client()

if __name__ == "__main__":
    unittest.main()