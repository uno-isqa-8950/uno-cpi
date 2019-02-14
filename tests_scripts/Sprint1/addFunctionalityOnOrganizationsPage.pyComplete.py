import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

class addFunctionality(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()


    def test_website(self):
        user1 = "doris123@yahoo.edu"
        pwd1 = "doris123!"
        fname = "Doriae"
        lname = "Alexa"
        email = "doris123@yahoo.edu"
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/")

        # Create a campus partner with one contact
        driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/a").click()
        driver.get("http://127.0.0.1:8000/partners/registerCampusPartner/")
        time.sleep(5)
        elem = driver.find_element_by_xpath("//*[@id='id_name']")
        elem.send_keys('Caps12')  # After every test, put a different name here
        time.sleep(5)
        select = Select(driver.find_element_by_id('id_college_name'))
        select.select_by_index(2)
        select = Select(driver.find_element_by_id('id_form-0-contact_type'))
        select.select_by_index(1)
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-email_id"]')
        elem.send_keys('doris@gmail.edu')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-first_name"]')
        elem.send_keys('Doris')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-last_name"]')
        elem.send_keys('Uwaezuoke')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-work_phone"]')
        elem.send_keys('4234567890')
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/form/div/div/div[5]/div/button').click()
        time.sleep(1)

        # Create another campus partner with the same contact details or different

        driver.get("http://127.0.0.1:8000/partners/registerCampusPartner/")
        time.sleep(3)
        elem = driver.find_element_by_xpath("//*[@id='id_name']")
        elem.send_keys('Stones12')  # After every test, put a different name here
        time.sleep(5)
        select = Select(driver.find_element_by_id('id_college_name'))
        select.select_by_index(2)
        select = Select(driver.find_element_by_id('id_form-0-contact_type'))
        select.select_by_index(1)
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-email_id"]')
        elem.send_keys('test@gmail.edu')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-first_name"]')
        elem.send_keys('Alex')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-last_name"]')
        elem.send_keys('Will')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-work_phone"]')
        elem.send_keys('4987654321')
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/form/div/div/div[5]/div/button').click()
        time.sleep(5)

        #create a campus partner user
        driver.get('http://127.0.0.1:8000/account/loginPage/')
        driver.get('http://127.0.0.1:8000/registerCampusPartnerUser/')
        time.sleep(2)
        select=Select(driver.find_element_by_id('id_campus_partner'))
        select.select_by_index(115)
        time.sleep(3)
        elem = driver.find_element_by_xpath('//*[@id="id_first_name"]')
        elem.send_keys(fname)
        elem = driver.find_element_by_xpath('//*[@id="id_last_name"]')
        elem.send_keys(lname)
        elem = driver.find_element_by_xpath('//*[@id="id_email"]')
        elem.send_keys(email)
        elem = driver.find_element_by_xpath('//*[@id="id_password"]')
        elem.send_keys(pwd1)
        elem = driver.find_element_by_xpath('//*[@id="id_password2"]')
        elem.send_keys(pwd1)
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/form/p/button').click()
        time.sleep(3)

        #Login as campus partners user with new credentials
        driver.get('http://127.0.0.1:8000/account/loginPage/')
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/input[2]')
        elem.send_keys(user1)
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/input[3]')
        elem.send_keys(pwd1)
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/div[1]/div/p/button').click()
        time.sleep(2)
        #Join a new organization
        driver.get('http://127.0.0.1:8000/partners/profile/orgprofile/')
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[3]/a').click()
        time.sleep(2)
        select = Select(driver.find_element_by_id('id_campus_partner'))
        select.select_by_index(115)
        driver.get('http://127.0.0.1:8000/partners/profile/orgprofile/')
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[3]/a').click()
        time.sleep(2)
        select = Select(driver.find_element_by_id('id_campus_partner'))
        select.select_by_index(116)
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/p/button').click()
        time.sleep(5)