import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

class UnoCpi(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_website(self):
        user = "spatibandla@gmail.edu"
        pwd = "password1!"
        user1 = "spatibandla@unomaha.edu"
        pwd1 = "password"
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/")

        # Create a campus partner with one contact
        driver.find_element_by_xpath("//*[@id='target']/ul/li[3]/a").click()
        driver.get("http://127.0.0.1:8000/partners/registerCampusPartner/")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//*[@id='id_name']")
        elem.send_keys('CPACS')  # After every test, put a different name here
        time.sleep(1)
        select = Select(driver.find_element_by_id('id_college_name'))
        select.select_by_index(1)
        select = Select(driver.find_element_by_id('id_form-0-contact_type'))
        select.select_by_index(2)
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-email_id"]')
        elem.send_keys('spatibandla@gmail.edu')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-first_name"]')
        elem.send_keys('Shashank')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-last_name"]')
        elem.send_keys('Patibandla')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-work_phone"]')
        elem.send_keys('1234567890')
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/form/div/div/div[5]/div/button').click()
        time.sleep(1)

        # Create another campus partner with the same contact details or different
        driver.get("http://127.0.0.1:8000/partners/registerCampusPartner/")
        time.sleep(1)
        elem = driver.find_element_by_xpath("//*[@id='id_name']")
        elem.send_keys('HPER')  # After every test, put a different name here
        time.sleep(1)
        select = Select(driver.find_element_by_id('id_college_name'))
        select.select_by_index(1)
        select = Select(driver.find_element_by_id('id_form-0-contact_type'))
        select.select_by_index(2)
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-email_id"]')
        elem.send_keys('test@gmail.edu')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-first_name"]')
        elem.send_keys('tester')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-last_name"]')
        elem.send_keys('test')
        elem = driver.find_element_by_xpath('//*[@id="id_form-0-work_phone"]')
        elem.send_keys('0987654321')
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/form/div/div/div[5]/div/button').click()
        time.sleep(1)

        #Login as admin and add those two campus partners to a campus partner user
        driver.get('http://127.0.0.1:8000/account/loginPage/')
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/input[2]')
        elem.send_keys(user1)
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/input[3]')
        elem.send_keys(pwd1)
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/div[1]/div/p/button').click()
        driver.get('http://127.0.0.1:8000/admin/partners/campuspartneruser/')
        driver.get('http://127.0.0.1:8000/admin/partners/campuspartneruser/add')
        driver.find_element_by_xpath('//*[@id="id_campus_partner"]/option[93]').click()
        driver.find_element_by_xpath('//*[@id="id_user"]/option[2]').click()
        driver.find_element_by_xpath('//*[@id="campuspartneruser_form"]/div/div/input[2]').click()
        driver.find_element_by_xpath('//*[@id="id_campus_partner"]/option[94]').click()
        driver.find_element_by_xpath('//*[@id="id_user"]/option[2]').click()
        driver.find_element_by_xpath('//*[@id="campuspartneruser_form"]/div/div/input[1]').click()
        driver.get('http://127.0.0.1:8000/admin/')
        driver.find_element_by_xpath('//*[@id="user-tools"]/a[2]').click()

        #Now check if the campus partner user that you associated the two campus partners has two organizations on the orgnizations or not
        #need to login as that campus partner user
        driver.get('http://127.0.0.1:8000/account/loginPage/')
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/input[2]')
        elem.send_keys(user)
        elem = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/input[3]')
        elem.send_keys(pwd)
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/div[1]/div/p/button').click()
        driver.get('http://127.0.0.1:8000/partners/profile/orgprofile/')
        time.sleep(10)