from tests_scripts import *
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os


class CSVDownloadButtonOnAllProjectsPage(unittest.TestCase):

    def test_CSV_Download_Button_On_All_Projects(self):
        pathname = os.path.join(os.getcwd(), "chromedriver")
        download_path = "C:\\Users\\Edem\\Downloads"
        driver = webdriver.Chrome(pathname)
        self.email = campus_partner_user
        self.password = campus_partner_pwd
        count = 0

        driver.maximize_window()

        """
        Change between base_url(APP) and test_url(LOCAL) if testing locally or the app
        """
        driver.get(sta_url)
        time.sleep(2)
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys(self.email)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(self.password)
        driver.find_element_by_name("password").send_keys(Keys.ENTER)

        # Click on Projects
        driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/a").click()
        # Click on All Projects
        driver.find_element_by_xpath("//A[@class='dropdown-item'][text()='My Projects']/preceding-sibling::A").click()

        self.assertEqual(driver.current_url, sta_url + "allProjects/")
        # Select the CSV download button
        driver.find_element_by_xpath("//SELECT[@name='example_length']/../../..//SPAN[text()='CSV']").click()
        # time.sleep(9)

        for fname in os.listdir(download_path):
            if fname.startswith("Community Partnership Initiative") and fname.endswith(".csv"):
                count += 1
                if count > 0:
                    self.assertTrue("Download Successful")
                else:
                    self.assertFalse("Download Failed")


