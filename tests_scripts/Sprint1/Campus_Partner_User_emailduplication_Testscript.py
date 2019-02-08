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
        user = "kjhamishra@unomaha.edu"
        pwd = "LakshyaKaavya1"
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/")


        #clicks on register
        elem = driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/a").click()
        #clicks on campus partner
        elem = driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/div/a[1]").click()
        #fills in campus partner name
        elem = driver.find_element_by_id("id_name")
        elem.send_keys("RegisterName1")
        #for College Name
        elem = driver.find_element_by_xpath('//*[@id="id_college_name"]/option[2]').click()
        #for Contact Type
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-contact_type"]/option[2]').click()
        #for contact email
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-email_id"]')
        elem.send_keys("drl@gmail.edu")
        #For contact first name
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-first_name"]')
        elem.send_keys("contactfirstname")
        #For contact last name
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-last_name"]')
        elem.send_keys("lastname")
        #for contact phone number
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-work_phone"]')
        elem.send_keys("402-333-4444")


        #clicks on submit form button
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/form/div/div/div[5]/div/button").click()
        time.sleep(3)

        # clicks on register
        elem = driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/a").click()
        # clicks on campus partner
        elem = driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/div/a[1]").click()
        # fills in campus partner name
        elem = driver.find_element_by_id("id_name")
        elem.send_keys("RegisterName2")
        # for College Name
        elem = driver.find_element_by_xpath('//*[@id="id_college_name"]/option[3]').click()
        # for Contact Type
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-contact_type"]/option[2]').click()
        # for contact email
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-email_id"]')
        elem.send_keys("drl@gmail.edu")
        # For contact first name
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-first_name"]')
        elem.send_keys("contactfirstname")
        # For contact last name
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-last_name"]')
        elem.send_keys("lastname")
        # for contact phone number
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-work_phone"]')
        elem.send_keys("402-333-4444")

        # clicks on submit form button
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/form/div/div/div[5]/div/button").click()
        time.sleep(3)

        driver.find_element_by_xpath('//*[@id="target"]/ul/li[4]/a').click()
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[2]")
        elem.send_keys(user)
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[3]")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        assert "Logged In"
        time.sleep(3)

        #goes to campus partner users page
        driver.get("http://127.0.0.1:8000/admin/partners/campuspartneruser/")
        time.sleep(2)
        #clicks on add campus partner user
        elem = driver.find_element_by_xpath('//*[@id="content-main"]/ul/li/a').click()
        time.sleep(3)
        #fills in campus partner
        elem = driver.find_element_by_id("id_campus_partner")
        elem.send_keys("Journalism")
        time.sleep(3)
        #fills in user field
        elem = driver.find_element_by_id("id_user")
        elem.send_keys("kjhamishra@unomaha.edu")
        #clicks save button
        elem = driver.find_element_by_xpath('/html/body/div/div[3]/div/form/div/div/input[1]').click()

        # goes to campus partner users page
        driver.get("http://127.0.0.1:8000/admin/partners/campuspartneruser/")
        time.sleep(2)
        # clicks on add campus partner user
        elem = driver.find_element_by_xpath('//*[@id="content-main"]/ul/li/a').click()
        time.sleep(3)
        # fills in campus partner
        elem = driver.find_element_by_id("id_campus_partner")
        elem.send_keys("Honors Program")
        time.sleep(3)
        # fills in user field
        elem = driver.find_element_by_id("id_user")
        elem.send_keys("kjhamishra@unomaha.edu")
        # clicks save button
        elem = driver.find_element_by_xpath('/html/body/div/div[3]/div/form/div/div/input[1]').click()










