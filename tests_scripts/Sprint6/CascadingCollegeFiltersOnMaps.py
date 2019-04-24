from tests_scripts import *
import unittest
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import os


class CascadingCollegeFiltersOnMaps(unittest.TestCase):
    def setUp(self):
        pathname = os.path.join(os.getcwd(), "chromedriver")
        self.driver = webdriver.Chrome(pathname)

    def test_cascading_filters_on_maps(self):
        driver = self.driver
        # self.email = community_partner_user
        # self.password = community_partner_pwd

        driver.maximize_window()

        driver.get(sta_url + 'communityPartner')
        # Select Menu
        driver.find_element_by_xpath("//IMG[@class='himg']/../../..//I[@class='fa fa-align-justify']").click()
        # Select All Campus Partners with All Colleges selected
        driver.find_element_by_xpath("//SELECT[@id='selectCollege']/following-sibling::SELECT").click()
        time.sleep(3)
        # Select A College and check out the campus partners changes
        selectcollege = Select(driver.find_element_by_id('selectCollege'))
        # Select a college
        selectcollege.select_by_index(1)
        time.sleep(3)
        # Select All Campus Partners to see the campus partners associated with the Colleges
        driver.find_element_by_xpath("//SELECT[@id='selectCollege']/following-sibling::SELECT").click()
        time.sleep(3)
        # Select another college
        selectcollege.select_by_index(2)
        time.sleep(3)
        # Select All Campus Partners to see the campus partners associated with the Colleges
        driver.find_element_by_xpath("//SELECT[@id='selectCollege']/following-sibling::SELECT").click()
        time.sleep(3)

        driver.get(sta_url + 'legislativeDistrict')
        # Select Menu
        driver.find_element_by_xpath("//IMG[@class='himg']/../../..//I[@class='fa fa-align-justify']").click()
        # Select All Campus Partners with All Colleges selected
        driver.find_element_by_xpath("//SELECT[@id='selectCollege']/following-sibling::SELECT").click()
        time.sleep(3)
        # Select A College and check out the campus partners changes
        selectcollege = Select(driver.find_element_by_id('selectCollege'))
        # Select a college
        selectcollege.select_by_index(1)
        time.sleep(3)
        # Select All Campus Partners to see the campus partners associated with the Colleges
        driver.find_element_by_xpath("//SELECT[@id='selectCollege']/following-sibling::SELECT").click()
        time.sleep(3)
        # Select another college
        selectcollege.select_by_index(2)
        time.sleep(3)
        # Select All Campus Partners to see the campus partners associated with the Colleges
        driver.find_element_by_xpath("//SELECT[@id='selectCollege']/following-sibling::SELECT").click()
        time.sleep(3)

        driver.get(sta_url + 'communityPartnerType')
        # Select Menu
        driver.find_element_by_xpath("//IMG[@class='himg']/../../..//I[@class='fa fa-align-justify']").click()
        # Select All Campus Partners with All Colleges selected
        driver.find_element_by_xpath("//SELECT[@id='selectCollege']/following-sibling::SELECT").click()
        time.sleep(3)
        # Select A College and check out the campus partners changes
        selectcollege = Select(driver.find_element_by_id('selectCollege'))
        # Select a college
        selectcollege.select_by_index(1)
        time.sleep(3)
        # Select All Campus Partners to see the campus partners associated with the Colleges
        driver.find_element_by_xpath("//SELECT[@id='selectCollege']/following-sibling::SELECT").click()
        time.sleep(3)
        # Select another college
        selectcollege.select_by_index(2)
        time.sleep(3)
        # Select All Campus Partners to see the campus partners associated with the Colleges
        driver.find_element_by_xpath("//SELECT[@id='selectCollege']/following-sibling::SELECT").click()
        time.sleep(3)

        driver.get(sta_url + 'projectMap')
        # Select Menu
        driver.find_element_by_xpath("//IMG[@class='himg']/../../..//I[@class='fa fa-align-justify']").click()
        # Select All Campus Partners with All Colleges selected
        driver.find_element_by_xpath("//SELECT[@id='selectCollege']/following-sibling::SELECT").click()
        time.sleep(3)
        # Select A College and check out the campus partners changes
        selectcollege = Select(driver.find_element_by_id('selectCollege'))
        # Select a college
        selectcollege.select_by_index(1)
        time.sleep(3)
        # Select All Campus Partners to see the campus partners associated with the Colleges
        driver.find_element_by_xpath("//SELECT[@id='selectCollege']/following-sibling::SELECT").click()
        time.sleep(3)
        # Select another college
        selectcollege.select_by_index(2)
        time.sleep(3)
        # Select All Campus Partners to see the campus partners associated with the Colleges
        driver.find_element_by_xpath("//SELECT[@id='selectCollege']/following-sibling::SELECT").click()
        time.sleep(3)

    def tearDown(self):
        self.driver.close()
        self.driver.stop_client()


if __name__ == "__main__":
    unittest.main()
