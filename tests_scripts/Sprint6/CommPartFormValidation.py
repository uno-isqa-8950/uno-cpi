from tests_scripts import *
import unittest
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import os


class CommunityPartnerFormValidation(unittest.TestCase):
    def setUp(self):
        pathname = os.path.join(os.getcwd(), "chromedriver")
        self.driver = webdriver.Chrome(pathname)

    def test_url_validation_unhappy_path(self):
        driver = self.driver
        url1 = 'unomaha.edu'
        url2 = 'http://unomaha.edu'
        url3 = 'https://unomaha.edu'

        driver.maximize_window()

        # Without login
        driver.get(sta_url + 'partners/registerCommunityPartner')
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").click()
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").clear()
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").send_keys('EdemTest1100')

        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url1)
        time.sleep(3)
        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'http://' + url1)

        Select(driver.find_element_by_id("id_community_type")).select_by_visible_text("Nonprofit")

        driver.find_element_by_id("id_address_line1").send_keys('8509 Maple Court')
        driver.find_element_by_id("id_city").send_keys('Quebec1')
        driver.find_element_by_id("id_state").send_keys('NE1')
        driver.find_element_by_id("id_zip").send_keys('68128')
        driver.find_element_by_id("id_country").send_keys('Canada')

        driver.find_element_by_xpath("//INPUT[@id='id_contact-0-email_id']/../../../..//SELECT[@id='id_contact-0-contact_type']").click()
        driver.find_element_by_xpath("//SELECT[@id='id_contact-0-contact_type']/../../../..//INPUT[@id='id_contact-0-email_id']").send_keys('edem@edem.com')
        driver.find_element_by_xpath("//INPUT[@id='id_contact-0-last_name']/../../../..//INPUT[@id='id_contact-0-first_name']").send_keys('Edem1')
        driver.find_element_by_xpath("//INPUT[@id='id_contact-0-first_name']/../../../..//INPUT[@id='id_contact-0-last_name']").send_keys("Dosseh1")
        driver.find_element_by_xpath("//INPUT[@id='id_contact-0-cell_phone']/../../../..//INPUT[@id='id_contact-0-work_phone']").send_keys('4021111111')

        Select(driver.find_element_by_id("id_primary_mission-0-mission_area")).select_by_visible_text("Social Justice")
        # Terms
        driver.find_element_by_xpath('//*[@id="terms"]').click()
        #Submit
        driver.find_element_by_xpath("//INPUT[@id='terms']/../../..//BUTTON[@type='submit']").click()

        bad_city = driver.find_element_by_xpath(
            "/html/body/div/div/div/div/div/div/div[2]/form/div[1]"
            "/div/div[3]/div[1]/div[2]/strong").text

        bad_state = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div[2]"
                                                 "/form/div[1]/div/div[3]/div[2]/div[2]/strong").text

        bad_first_name = driver.find_element_by_xpath('//*[@id="contact1"]'
                                                      '/div[3]/div[1]/div[2]/strong').text

        bad_last_name = driver.find_element_by_xpath('//*[@id="contact1"]/div[3]'
                                                     '/div[2]/div[2]/strong').text

        print(bad_city)
        print(bad_state)
        print(bad_first_name)
        print(bad_last_name)

        self.assertTrue(bad_city != '')
        self.assertTrue(bad_state != '')
        self.assertTrue(bad_first_name != '')
        self.assertTrue(bad_last_name != '')

    def test_url_validation_non_url(self):
        driver = self.driver
        url1 = 'unomaha.edu'
        url2 = 'http://unomaha.edu'
        url3 = 'https://unomaha.edu'

        driver.maximize_window()

        # Without login
        driver.get(sta_url + 'partners/registerCommunityPartner')
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").click()
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").clear()
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").send_keys('EdemTest1100')

        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url1)
        time.sleep(3)
        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'http://' + url1)
        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url2)
        time.sleep(3)
        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'http://' + url2)
        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url3)
        time.sleep(3)
        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'https://' + url3)
        # Clearing URL
        driver.find_element_by_name("website_url").clear()
        Select(driver.find_element_by_id("id_community_type")).select_by_visible_text("Nonprofit")

        driver.find_element_by_id("id_address_line1").send_keys('8509 Maple Court')
        driver.find_element_by_id("id_city").send_keys('Omaha')
        driver.find_element_by_id("id_state").send_keys('NE')
        driver.find_element_by_id("id_zip").send_keys('68128')
        driver.find_element_by_id("id_country").send_keys('USA')

        driver.find_element_by_xpath("//INPUT[@id='id_contact-0-email_id']/../../../..//SELECT[@id='id_contact-0-contact_type']").click()
        driver.find_element_by_xpath("//SELECT[@id='id_contact-0-contact_type']/../../../..//INPUT[@id='id_contact-0-email_id']").send_keys('edem@edem.com')
        driver.find_element_by_xpath("//INPUT[@id='id_contact-0-last_name']/../../../..//INPUT[@id='id_contact-0-first_name']").send_keys('Edem')
        driver.find_element_by_xpath("//INPUT[@id='id_contact-0-first_name']/../../../..//INPUT[@id='id_contact-0-last_name']").send_keys("Dosseh")
        driver.find_element_by_xpath("//INPUT[@id='id_contact-0-cell_phone']/../../../..//INPUT[@id='id_contact-0-work_phone']").send_keys('4021111111')

        Select(driver.find_element_by_id("id_primary_mission-0-mission_area")).select_by_visible_text("Social Justice")
        # Terms
        driver.find_element_by_xpath('//*[@id="terms"]').click()
        #Submit
        driver.find_element_by_xpath("//INPUT[@id='terms']/../../..//BUTTON[@type='submit']").click()

    def test_url_validation(self):
        driver = self.driver
        url1 = 'unomaha.edu'
        url2 = 'http://unomaha.edu'
        url3 = 'https://unomaha.edu'

        driver.maximize_window()

        # Without login
        driver.get(sta_url + 'partners/registerCommunityPartner')
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").click()
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").clear()
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").send_keys('EdemTest1200')

        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url1)
        time.sleep(3)
        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'http://' + url1)
        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url2)
        time.sleep(3)
        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'http://' + url2)
        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url3)
        time.sleep(3)
        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'https://' + url3)

        Select(driver.find_element_by_id("id_community_type")).select_by_visible_text("Nonprofit")

        driver.find_element_by_id("id_address_line1").send_keys('8509 Maple Court')
        driver.find_element_by_id("id_city").send_keys('Omaha')
        driver.find_element_by_id("id_state").send_keys('NE')
        driver.find_element_by_id("id_zip").send_keys('68128')
        driver.find_element_by_id("id_country").send_keys('USA')

        driver.find_element_by_xpath("//INPUT[@id='id_contact-0-email_id']/../../../..//SELECT[@id='id_contact-0-contact_type']").click()
        driver.find_element_by_xpath("//SELECT[@id='id_contact-0-contact_type']/../../../..//INPUT[@id='id_contact-0-email_id']").send_keys('edem@edem.com')
        driver.find_element_by_xpath("//INPUT[@id='id_contact-0-last_name']/../../../..//INPUT[@id='id_contact-0-first_name']").send_keys('Edem')
        driver.find_element_by_xpath("//INPUT[@id='id_contact-0-first_name']/../../../..//INPUT[@id='id_contact-0-last_name']").send_keys("Dosseh")
        driver.find_element_by_xpath("//INPUT[@id='id_contact-0-cell_phone']/../../../..//INPUT[@id='id_contact-0-work_phone']").send_keys('4021111111')

        Select(driver.find_element_by_id("id_primary_mission-0-mission_area")).select_by_visible_text("Social Justice")
        # Terms
        driver.find_element_by_xpath('//*[@id="terms"]').click()
        #Submit
        driver.find_element_by_xpath("//INPUT[@id='terms']/../../..//BUTTON[@type='submit']").click()

    def test_with_users(self):
        driver = self.driver
        url1 = 'unomaha.edu'
        url2 = 'http://unomaha.edu'
        url3 = 'https://unomaha.edu'

        driver.maximize_window()

        # Campus partner login
        driver.get(sta_url + 'login/')
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys(campus_partner_user)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(campus_partner_pwd)
        driver.find_element_by_name("password").send_keys(Keys.ENTER)

        driver.get(sta_url + 'partners/registerCommunityPartner')
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").click()
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").clear()
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").send_keys('EdemTest106')

        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url1)
        time.sleep(3)
        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'https://' + url1)
        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url2)
        time.sleep(3)
        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'http://' + url2)
        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url3)
        time.sleep(3)
        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'https://' + url3)

        Select(driver.find_element_by_id("id_community_type")).select_by_visible_text("Nonprofit")

        driver.find_element_by_id("id_address_line1").send_keys('8509 Maple Court')
        driver.find_element_by_id("id_city").send_keys('Omaha')
        driver.find_element_by_id("id_state").send_keys('NE')
        driver.find_element_by_id("id_zip").send_keys('68128')
        driver.find_element_by_id("id_country").send_keys('USA')

        driver.find_element_by_xpath(
            "//INPUT[@id='id_contact-0-email_id']/../../../..//SELECT[@id='id_contact-0-contact_type']").click()
        driver.find_element_by_xpath(
            "//SELECT[@id='id_contact-0-contact_type']/../../../..//INPUT[@id='id_contact-0-email_id']").send_keys(
            'edem@edem.com')
        driver.find_element_by_xpath(
            "//INPUT[@id='id_contact-0-last_name']/../../../..//INPUT[@id='id_contact-0-first_name']").send_keys('Edem')
        driver.find_element_by_xpath(
            "//INPUT[@id='id_contact-0-first_name']/../../../..//INPUT[@id='id_contact-0-last_name']").send_keys(
            "Dosseh")
        driver.find_element_by_xpath(
            "//INPUT[@id='id_contact-0-cell_phone']/../../../..//INPUT[@id='id_contact-0-work_phone']").send_keys(
            '4021111111')

        Select(driver.find_element_by_id("id_primary_mission-0-mission_area")).select_by_visible_text("Social Justice")
        # Terms
        driver.find_element_by_xpath('//*[@id="terms"]').click()
        # Submit
        driver.find_element_by_xpath("//INPUT[@id='terms']/../../..//BUTTON[@type='submit']").click()

        # campus_partner_user logout:
        driver.find_element_by_xpath("(//A[@class='nav-link dropdown-toggle'])[4]").click()
        driver.find_element_by_xpath('//*[@id="target"]/ul/li[5]/div/a[3]').click()
        assert sta_url + "logout/" in driver.current_url

        # Community partner login
        driver.get(sta_url + 'login/')
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys(community_partner_user)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(community_partner_pwd)
        driver.find_element_by_name("password").send_keys(Keys.ENTER)

        driver.get(sta_url + 'partners/registerCommunityPartner')
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").click()
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").clear()
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").send_keys('EdemTest107')

        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url1)
        time.sleep(3)
        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'https://' + url1)
        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url2)
        time.sleep(3)
        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'http://' + url2)
        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url3)
        time.sleep(3)
        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'https://' + url3)

        Select(driver.find_element_by_id("id_community_type")).select_by_visible_text("Nonprofit")

        driver.find_element_by_id("id_address_line1").send_keys('8509 Maple Court')
        driver.find_element_by_id("id_city").send_keys('Omaha')
        driver.find_element_by_id("id_state").send_keys('NE')
        driver.find_element_by_id("id_zip").send_keys('68128')
        driver.find_element_by_id("id_country").send_keys('USA')

        driver.find_element_by_xpath(
            "//INPUT[@id='id_contact-0-email_id']/../../../..//SELECT[@id='id_contact-0-contact_type']").click()
        driver.find_element_by_xpath(
            "//SELECT[@id='id_contact-0-contact_type']/../../../..//INPUT[@id='id_contact-0-email_id']").send_keys(
            'edem@edem.com')
        driver.find_element_by_xpath(
            "//INPUT[@id='id_contact-0-last_name']/../../../..//INPUT[@id='id_contact-0-first_name']").send_keys('Edem')
        driver.find_element_by_xpath(
            "//INPUT[@id='id_contact-0-first_name']/../../../..//INPUT[@id='id_contact-0-last_name']").send_keys(
            "Dosseh")
        driver.find_element_by_xpath(
            "//INPUT[@id='id_contact-0-cell_phone']/../../../..//INPUT[@id='id_contact-0-work_phone']").send_keys(
            '4021111111')

        Select(driver.find_element_by_id("id_primary_mission-0-mission_area")).select_by_visible_text("Social Justice")
        # Terms
        driver.find_element_by_xpath('//*[@id="terms"]').click()
        # Submit
        driver.find_element_by_xpath("//INPUT[@id='terms']/../../..//BUTTON[@type='submit']").click()

        # community_partner_user logout:
        driver.find_element_by_xpath("((//A[@class='nav-link'])[2]/../..//A[@class='nav-link dropdown-toggle'])[3]").click()
        driver.find_element_by_xpath("(//SPAN[@id='pic']/../..//A[@class='dropdown-item'])[3]").click()
        assert sta_url + "logout/" in driver.current_url

        # Admin partner login
        driver.get(sta_url + 'login/')
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys(admin_user)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(admin_pwd)
        driver.find_element_by_name("password").send_keys(Keys.ENTER)

        driver.get(sta_url + 'partners/registerCommunityPartner')
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").click()
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").clear()
        driver.find_element_by_xpath("//INPUT[@id='id_website_url']/../../../../..//INPUT[@id='id_name']").send_keys('EdemTest109')

        driver.find_element_by_name("website_url").click()
        driver.find_element_by_name("website_url").clear()
        driver.find_element_by_name("website_url").send_keys(url1)

        self.assertTrue(driver.find_element_by_name("website_url").get_attribute('value'), 'https://' + url1)

        Select(driver.find_element_by_id("id_community_type")).select_by_visible_text("Nonprofit")

        driver.find_element_by_id("id_address_line1").send_keys('8509 Maple Court')
        driver.find_element_by_id("id_city").send_keys('Omaha')
        driver.find_element_by_id("id_state").send_keys('NE')
        driver.find_element_by_id("id_zip").send_keys('68128')
        driver.find_element_by_id("id_country").send_keys('USA')

        driver.find_element_by_xpath(
            "//INPUT[@id='id_contact-0-email_id']/../../../..//SELECT[@id='id_contact-0-contact_type']").click()
        driver.find_element_by_xpath(
            "//SELECT[@id='id_contact-0-contact_type']/../../../..//INPUT[@id='id_contact-0-email_id']").send_keys(
            'edem@edem.com')
        driver.find_element_by_xpath(
            "//INPUT[@id='id_contact-0-last_name']/../../../..//INPUT[@id='id_contact-0-first_name']").send_keys('Edem')
        driver.find_element_by_xpath(
            "//INPUT[@id='id_contact-0-first_name']/../../../..//INPUT[@id='id_contact-0-last_name']").send_keys(
            "Dosseh")
        driver.find_element_by_xpath(
            "//INPUT[@id='id_contact-0-cell_phone']/../../../..//INPUT[@id='id_contact-0-work_phone']").send_keys(
            '4021111111')

        Select(driver.find_element_by_id("id_primary_mission-0-mission_area")).select_by_visible_text("Social Justice")

        # Terms
        driver.find_element_by_xpath('//*[@id="terms"]').click()
        # Submit
        driver.find_element_by_xpath("//INPUT[@id='terms']/../../..//BUTTON[@type='submit']").click()

        # Check Community Partners
        driver.find_element_by_xpath("(//A[@class='nav-link']/../..//A[@class='nav-link dropdown-toggle'])[4]").click()
        driver.find_element_by_xpath("(//A[@class='nav-link dropdown-toggle'])[4]"
                                     "/..//A[@class='dropdown-item'][text()='Admin View']").click()

        driver.get('https://uno-cpi-sta.herokuapp.com/admin/partners/communitypartner/')

        driver.find_element_by_xpath("//INPUT[@type='submit']/preceding-sibling::INPUT").click()
        driver.find_element_by_xpath("//INPUT[@type='submit']/preceding-sibling::INPUT").send_keys('Edem')

        driver.find_element_by_xpath("//INPUT[@id='searchbar']/following-sibling::INPUT").click()

        time.sleep(10)

    def tearDown(self):
        self.driver.close()
        self.driver.stop_client()


if __name__ == "__main__":
    unittest.main()
