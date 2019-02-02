import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By



class admin_login(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='C:\Webdrivers/chromedriver.exe')

    def test_blog(self):
        user = "drljha@gmail.edu"
        pwd = "LakshyaKaavya1*"
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/")
        time.sleep(3)

        elem = driver.find_element_by_xpath("//*[@id='target']/ul/li[4]/a").click()
        time.sleep(2)
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[2]")
        elem.send_keys(user)
        time.sleep(2)
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[3]")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        assert "Logged In"
        time.sleep(1)
        #xpath, clicks on project button
        elem = driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/a").click()
        time.sleep(1)
        #clicks on create project button
        elem = driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/div/a[3]").click()
        time.sleep(1)
        elem = driver.find_element_by_id("id_project_name")
        elem.send_keys("Lecture on Human Rights")
        #for Engagement type
        elem = driver.find_element_by_xpath('//*[@id="id_engagement_type"]/option[2]').click()
        time.sleep(1)
        #for Activity Type
        elem = driver.find_element_by_xpath('//*[@id="id_activity_type"]/option[3]').click()
        time.sleep(2)
        #for campus partner information
        elem = driver.find_element_by_xpath("//*[@id='id_form-0-campus_partner']/option[5]").click()
        time.sleep(2)
        #For Status
        driver.find_element_by_id("select2-id_status-container").click()
        time.sleep(2)
        #For semester
        elem = driver.find_element_by_id("id_semester")
        elem.send_keys("Spring")
        time.sleep(2)
        #for academic year
        driver.find_element_by_id("select2-id_academic_year-container").click()
        time.sleep(2)
        #for address
        elem = driver.find_element_by_id("id_address_line1")
        elem.send_keys("171 Q st")
        time.sleep(2)
        elem = driver.find_element_by_id("id_city")
        elem.send_keys("Omaha")
        time.sleep(2)
        elem = driver.find_element_by_id("id_state")
        elem.send_keys("NE")
        time.sleep(2)
        elem = driver.find_element_by_id("id_country")
        elem.send_keys("USA")
        time.sleep(2)
        elem = driver.find_element_by_id("id_zip")
        elem.send_keys("68135")

        time.sleep(2)
        #for mission type
        elem = driver.find_element_by_xpath("//*[@id='id_form-0-mission_type']")
        elem.send_keys("Primary")
        time.sleep(2)
        #for mission area
        elem = driver.find_element_by_xpath("//*[@id='id_form-0-mission']")
        elem.send_keys("Educational Support")
        time.sleep(2)
        #clicks on submit form button
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/form/div[6]/div/button").click()
        time.sleep(3)






    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

