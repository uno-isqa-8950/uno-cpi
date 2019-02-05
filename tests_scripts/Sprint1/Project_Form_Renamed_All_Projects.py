import unittest
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import os
from tests_scripts import *


class ProjectFormRenamed(unittest.TestCase):
    pathname = os.path.join(os.getcwd(), "chromedriver")
    driver = webdriver.Chrome(pathname)

    webdriver.support.ui
    def setUp(self):

        self.driver = webdriver.Chrome()
        self.email = "aanzalone@unomaha.edu"
        self.password = "Capstone2019!"

    def test_Project_Renamed_AllProjects(self):
        driver = self.driver
        test_url = url
        driver.maximize_window()

        """
        Change between base_url(APP) and test_url(LOCAL) if testing locally or the app
        """
        driver.get(test_url)
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys(self.email)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(self.password)
        driver.find_element_by_name("password").send_keys(Keys.ENTER)
        driver.find_element_by_xpath("(//a[contains(@href, '#')])[5]").click()
        """
        Asserting DropDown Tab is named Projects
        """
        dropdown_text = driver.find_element_by_xpath("(//a[contains(@href, '#')])[5]").text
        self.assertEqual("Project", dropdown_text )

        """
        Select "All Projects" in DropDown Tab is named Projects and asserting the text is "All Projects"
        """
        dropdown_list = driver.find_element_by_xpath("//div[@id='target']/ul/li[3]/div/a").text
        self.assertEqual("All Projects", dropdown_list)
        driver.find_element_by_xpath("//div[@id='target']/ul/li[3]/div/a").send_keys(Keys.ENTER)
        assert test_url + "projectSearch/" in driver.current_url
        """
        Asserting page is renamed "All Projects"
        """
        self.assertEqual("All Projects",driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[1]/h4").text)



    def tearDown(self):
        self.driver.close()
        self.driver.stop_client()

if __name__ == "__main__":
    unittest.main()