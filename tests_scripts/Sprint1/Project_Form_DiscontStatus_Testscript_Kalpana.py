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

        driver.find_element_by_xpath("//*[@id='target']/ul/li[4]/a").click()
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[2]")
        elem.send_keys(user)
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[3]")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        assert "Logged In"
        # xpath, clicks on project button
        driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/a").click()
        # clicks on create project button
        driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/div/a[3]").click()
        elem = driver.find_element_by_id("id_project_name")
        elem.send_keys("Human Rights Test Project 3")
        # for Engagement type
        driver.find_element_by_xpath('//*[@id="id_engagement_type"]/option[2]').click()
        # for Activity Type
        driver.find_element_by_xpath('//*[@id="id_activity_type"]/option[2]').click()
        # for Status
        driver.find_element_by_xpath('//*[@id="id_status"]/option[4]').click()
        # For semester
        elem = driver.find_element_by_id("id_semester")
        elem.send_keys("Spring")
        # for academic year
        driver.find_element_by_xpath('//*[@id="id_academic_year"]/option[3]').click()
        #for address
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


        #clicks on submit form button
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/form/div[8]/div/button").click()



    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

