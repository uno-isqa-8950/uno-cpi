import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By



class admin_login(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_blog(self):
        user = " "  #campus partner user
        pwd = " "   #campus partner pwd
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
        #xpath, clicks on project button
        driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/a").click()
        #clicks on create project button
        driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/div/a[3]").click()
        elem = driver.find_element_by_id("id_project_name")
        elem.send_keys("Test Project")
        #for Engagement type
        driver.find_element_by_xpath('//*[@id="id_engagement_type"]/option[2]').click()
        #for Activity Type
        driver.find_element_by_xpath('//*[@id="id_activity_type"]/option[3]').click()
        #for Status
        driver.find_element_by_xpath('//*[@id="id_status"]/option[2]').click()
        #For semester
        elem = driver.find_element_by_id("id_semester")
        elem.send_keys("Spring")
        #for academic year
        driver.find_element_by_xpath('//*[@id="id_academic_year"]/option[3]').click()
        #for address
        elem = driver.find_element_by_id("id_address_line1")
        elem.send_keys("Testing st")
        elem = driver.find_element_by_id("id_city")
        elem.send_keys("Omaha")
        elem = driver.find_element_by_id("id_state")
        elem.send_keys("NE")
        elem = driver.find_element_by_id("id_country")
        elem.send_keys("USA")
        elem = driver.find_element_by_id("id_zip")
        elem.send_keys("68135")

        #for mission
        driver.find_element_by_xpath('// *[ @ id = "contact1"] / div[3] / button').click()
        driver.find_element_by_xpath('//*[@id="id_mission-0-mission_type"]/option[2]').click()
        driver.find_element_by_xpath("//*[@id='id_mission-0-mission']/option[2]").click()
        driver.find_element_by_xpath('//*[@id="id_mission-1-mission_type"]/option[3]').click()
        driver.find_element_by_xpath("//*[@id='id_mission-1-mission']/option[3]").click()
        time.sleep(5)
        #for campus (make sure to select the option which is the campus partner of the testing user)
        driver.find_element_by_xpath("//button[@class='btn btn-secondary add-campus-row']").click()
        driver.find_element_by_xpath('//*[@id="id_campus-0-campus_partner"]/option[5]').click()
        driver.find_element_by_xpath('//*[@id="id_campus-1-campus_partner"]/option[2]').click()
        time.sleep(5)
        #for community
        driver.find_element_by_xpath("//button[@class='btn btn-secondary add-community-row']").click()
        driver.find_element_by_xpath('//*[@id="id_community-0-community_partner"]/option[4]').click()
        driver.find_element_by_xpath('//*[@id="id_community-1-community_partner"]/option[7]').click()
        time.sleep(5)
        #clicks on submit form button
        driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/form/div[11]/div/button").click()
        time.sleep(15)





    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

