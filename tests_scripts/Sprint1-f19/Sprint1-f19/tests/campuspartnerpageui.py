from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class CampusPartnersPageUi:
    ## URL
    URL = 'https://uno-cpi-dev.herokuapp.com/'

    ##locators for  Maps
    Partners_Homepagelink = (By.XPATH, '//*[@id="target"]/ul/li[3]/a')
    Partners_Registercampuspartnerlink = (By.XPATH, '//*[@id="myButton1"]')
    Partners_Campuspartnername = (By.XPATH, '//*[@id="id_name"]')
    Partners_College = (By.XPATH, '//*[@id="select2-id_college_name-container"]')
    Partners_next = (By.XPATH, '//*[@id="smartwizard"]/div[2]/div/button[2]')
    Partners_campusfirstname = (By.XPATH, '//*[@id="id_form-0-first_name"]')
    Partners_campuslastname = (By.XPATH, '//*[@id="id_form-0-last_name"]')
    Partners_campusemail = (By.XPATH, '//*[@id="id_form-0-email_id"]')
    Partners_addcampuscontact = (By.XPATH, '//*[@id="contactinfo"]/div/div[1]/div/button')
    Partners_campusterms = (By.XPATH, '//*[@id="terms"]')
    Partners_campussubmit = (By.XPATH, '//*[@id="submit"]')
    ### Initializer

    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods

    def load(self):
        self.browser.get(self.URL)

    ##partners link on home page

    def partners_homepage(self):
        Partners_Homepage = self.browser.find_element(*self.Partners_Homepagelink)
        Partners_Homepage.click()

    def partners_campuspartnerregister(self):
        Partners_Legislativedistrict = self.browser.find_element(*self.Partners_Registercampuspartnerlink)
        Partners_Legislativedistrict.click()


    def partners_Campuspartnername(self):
        Partners_Campuspartnername = self.browser.find_element(*self.Partners_Campuspartnername)
        Partners_Campuspartnername.send_keys("UNO" + Keys.RETURN)

    def partners_College(self):
        Partners_College = self.browser.find_element(*self.Partners_College)
        Partners_College.send_keys("College Of IS & T" + Keys.RETURN)

    def partners_next(self):
        Partners_next = self.browser.find_element(*self.Partners_next)
        Partners_next.click()

    def partners_campusfirstname(self):
        Partners_campusfirstname = self.browser.find_element(*self.Partners_campusfirstname)
        Partners_campusfirstname.send_keys("Divya" + Keys.RETURN)

    def partners_campuslastname(self):
        partners_campuslastname = self.browser.find_element(*self.Partners_campuslastname)
        partners_campuslastname.send_keys("Korrapati" + Keys.RETURN)

    def partners_campusemail(self):
        Partners_campusemail = self.browser.find_element(*self.Partners_campusemail)
        Partners_campusemail.send_keys("dkorrapati@unomaha.edu" + Keys.RETURN)

    def partners_addcampuscontact(self):
        Partners_addcampuscontact = self.browser.find_element(*self.Partners_addcampuscontact)
        Partners_addcampuscontact.click()

    def partners_campusterms(self):
        Partners_campusterms = self.browser.find_element(*self.Partners_campusterms)
        Partners_campusterms.click()

    def partners_campussubmit(self):
        Partners_campussubmit = self.browser.find_element(*self.Partners_campussubmit)
        Partners_campussubmit.click()