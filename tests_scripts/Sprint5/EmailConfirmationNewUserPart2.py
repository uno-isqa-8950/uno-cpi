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
        driver.get("https://urldefense.proofpoint.com/v2/url?u=http-3A__uno-2Dcpi-2Dsta.herokuapp.com_activate_MzE_556-2D5e235370a505d54c1938&d=DwICaQ&c=Cu5g146wZdoqVuKpTNsYHeFX_rg6kWhlkLF8Eft-wwo&r=e1ETXSw2aymaQuS5yJr5rkZ0fLYsLVSNUsJDiW-u9nY&m=xZiitkXthdROT9rxY-L92Kg4Giul0Tye_5tcS1ZKEMw&s=6JDb955DIvqYgvCj7dz1xZfeXmFOpW7jQYFlVfcQWeI&e=")
        time.sleep(7) #here we are getting the link from the email. This will automatically get us logged in as campus partner user.
        #you can logout from here and use the same credential to login again as a campus partner user


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

