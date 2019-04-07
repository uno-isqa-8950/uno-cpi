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
        user = "" #put user name
        pwd = "" #put password
        driver = self.driver
        driver.maximize_window()
        driver.get("https://uno-cpi-sta.herokuapp.com/account/loginPage/")
        time.sleep(1)

        driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/div[2]/div/a[2]").click()

        driver.find_element_by_xpath("//*[@id='id_campus_partner']/option[2]").click()
        time.sleep(1)

        elem = driver.find_element_by_id("id_first_name")
        elem.send_keys("Kaavyaa")
        elem = driver.find_element_by_id("id_last_name")
        elem.send_keys("Jha")
        elem = driver.find_element_by_id("id_email")
        elem.send_keys("kjhamishra@unomaha.edu")
        elem = driver.find_element_by_id("id_password")
        elem.send_keys("Capstone2019*")
        elem = driver.find_element_by_id("id_password2")
        elem.send_keys("Capstone2019*")

        #clicks on submit button
        driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/form/p/button").click()
        time.sleep(3)  # a message saying an email link needs to be clicked to confirm the user would be sent.

        #Lets try to sign up without clicking the link first

        driver.get("https://uno-cpi-sta.herokuapp.com/account/loginPage/")
        time.sleep(1)

        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[2]")
        elem.send_keys("kjhamishra@unomaha.edu")
        time.sleep(1)
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/input[3]")
        elem.send_keys("Capstone2019*")
        elem = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/div/form/div[1]/p/button").click()
        time.sleep(1)  # While trying to login without clicking the email link sent in an email it gives an error.

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

