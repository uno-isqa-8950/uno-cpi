from tests_scripts import *
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os


class CommPartnerOrgPage(unittest.TestCase):
    # def setUp(self):
    #     self.driver = webdriver.Chrome(executable_path='C:\Webdrivers/chromedriver.exe')

    def test_CommPartner_OrgPage(self):
        pathname = os.path.join(os.getcwd(), "chromedriver")
        driver = webdriver.Chrome(pathname)
        self.email = community_partner_user
        self.password = community_partner_pwd

        driver.maximize_window()

        """
        Change between base_url(APP) and test_url(LOCAL) if testing locally or the app
        """
        driver.get(test_url)
        time.sleep(2)
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys(self.email)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(self.password)
        driver.find_element_by_name("password").send_keys(Keys.ENTER)
        driver.find_element_by_xpath('//*[@id="target"]/ul/li[4]/a').click()
        driver.get('http://127.0.0.1:8000/partners/profile/orgprofile/')

        # Select Mission
        driver.find_element_by_xpath("//A[@href='/partners/profile/4/orgprofilecontacts/'][text()=' Contacts ']/../..//A[@href='/partners/profile/4/orgprofilemissions/'][text()=' Missions ']").click()
        time.sleep(5)
        driver.get('http://127.0.0.1:8000/partners/profile/orgprofile/')


        # Select Contacts
        driver.find_element_by_xpath("//A[@href='/partners/profile/4/orgprofilemissions/'][text()=' Missions ']/../..//A[@href='/partners/profile/4/orgprofilecontacts/'][text()=' Contacts ']").click()
        time.sleep(5)
        driver.get('http://127.0.0.1:8000/partners/profile/orgprofile/')


        # Select Organization
        driver.find_element_by_xpath("(//A[@href='/partners/profile/19/orgprofileupdate/'][text()=' Edit '][text()="
                                     "' Edit '])[2]"
                                     "/../../../../../../..//A[@href='/partners/orgprofile/partner_add/'][text()"
                                     "=' Join a Existing Community Partner Organization ']").click()
        time.sleep(5)
        driver.get('http://127.0.0.1:8000/partners/profile/orgprofile/')

        # Select Edit
        driver.find_element_by_xpath("//A[@href='/partners/profile/4/orgprofilecontacts/'][text()=' Contacts ']/../..//A[@href='/partners/profile/4/orgprofileupdate/'][text()=' Edit ']").click()
        time.sleep(5)
        driver.get('http://127.0.0.1:8000/partners/profile/orgprofile/')

        driver.close()


if __name__ == "__main__":
    unittest.main()