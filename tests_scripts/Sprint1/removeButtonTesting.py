import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class removeButtonTesting(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.url = "http://127.0.0.1:8000/"

    def test_ProjectRemove(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(self.url)

        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='target']/ul/li[4]/a").click()
        elem = driver.find_element_by_xpath("//input[@name='email']")
        elem.send_keys("aanzalone@unomaha.edu")
        elem = driver.find_element_by_xpath("//input[@name='password']")
        elem.send_keys("Capstone2019!")
        elem.send_keys(Keys.RETURN)
        assert "Logged In"

        #Open Project Form
        driver.find_element_by_xpath("//div[@id='target']/ul/li[3]/a").click()
        driver.find_element_by_xpath("//div[@id='target']/ul/li[3]/div/a[3]").click()
        #Click Add Mission Area
        driver.find_element_by_xpath("//div[@id='contact1']/div[3]/button").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/form/div[8]/div[3]/button").click()
        time.sleep(2)
        assert "Mission Area Passed"
        #Click Add Campus Partner
        driver.find_element_by_xpath("(//div[@id='contact1']/div[3]/button)[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/form/div[9]/div[3]/button").click()
        time.sleep(2)
        assert "Campus Partner Passed"
        #Click Add Community Partner
        driver.find_element_by_xpath("(//div[@id='contact1']/div[3]/button)[3]").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/form/div[10]/div[3]/button").click()
        time.sleep(2)
        assert "Community Partner Passed"

    def test_CampusPartner(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(self.url)

        #Open Campus Partner Registration Form
        driver.find_element_by_xpath("/html/body/nav/div/ul/li[3]/a").click()
        driver.find_element_by_xpath("/html/body/nav/div/ul/li[3]/div/a[1]").click()
        time.sleep(2)

        #Click Add Contact and Remove
        driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/form/div/div/div[4]/div[4]/button").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div/div/div/div/div/div[2]/form/div/div/div[4]/div[4]/button").click()
        time.sleep(2)
        assert "Campus Partner Registration Passed"

    def test_CommunityPartner(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(self.url)

        #Open Community Partner Registration Form
        driver.find_element_by_xpath("/html/body/nav/div/ul/li[3]/a").click()
        driver.find_element_by_xpath("/html/body/nav/div/ul/li[3]/div/a[2]").click()
        time.sleep(2)

        #Click Add Contact and Remove
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div[2]/form/div[2]/div[4]/button").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div[2]/form/div[2]/div[4]/button").click()
        time.sleep(2)

        #CLick Add Mission and Remove
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div[2]/form/div[3]/div[2]/button").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div[2]/form/div[3]/div[2]/button").click()
        time.sleep(2)
        assert "Community Parnter Registration Passed"

    def tearDown(self):
        self.driver.close()
        self.driver.stop_client()

if __name__ == "__main__":
    unittest.main()