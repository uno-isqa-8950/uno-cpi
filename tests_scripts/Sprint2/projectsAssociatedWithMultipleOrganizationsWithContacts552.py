import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

class projectAssociated(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()


    def test_website(self):
        user1 = "dominic@yahoo.edu"
        pwd1 = "password1!"
        fname = "Dominic"
        lname = "Lexas"
        email = user1
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/")


        #create a campus partner user
        driver.get('http://127.0.0.1:8000/account/loginPage/')
        driver.get('http://127.0.0.1:8000/registerCampusPartnerUser/')
        time.sleep(2)
        select = Select(driver.find_element_by_id('id_campus_partner'))
        select.select_by_index(90)
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
        elem = driver.find_element_by_xpath("//*[@id='id_campus_partner']")
        elem.send_keys('Aerospace Studies Department')  # After every test, put a different name here
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/p/button').click()
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[3]/a').click()
        elem = driver.find_element_by_xpath("//*[@id='id_campus_partner']")
        elem.send_keys('Service Learning Academy (SLA)')  # After every test, put a different name here
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/p/button').click()
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[3]/a').click()
        elem = driver.find_element_by_xpath("//*[@id='id_campus_partner']")
        elem.send_keys('HPER')  # After every test, put a different name here
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/p/button').click()

        #check that the individual organization has at least a contact
        driver.find_element_by_xpath('// *[ @ id = "example"] / tbody / tr[1] / td[4] / a').click()
        time.sleep(2)
        driver.get('http://127.0.0.1:8000/partners/profile/orgprofile/')
        driver.find_element_by_xpath('// *[ @ id = "example"] / tbody / tr[2] / td[4] / a').click()
        time.sleep(2)

        #edit an organization
        driver.get('http://127.0.0.1:8000/partners/profile/orgprofile/')
        driver.find_element_by_xpath('//*[@id="example"]/tbody/tr[3]/td[5]/a').click()
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/div[3]/div/div[2]/select')
        elem.send_keys('Athletics')
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/p/button').click()
        time.sleep(2)
        driver.get('http://127.0.0.1:8000/partners/profile/orgprofile/')
        time.sleep(2)

        #Confirm if all the edited organizations along with their projects are visible
        driver.get('http://127.0.0.1:8000/myProjects/')
        time.sleep(5)