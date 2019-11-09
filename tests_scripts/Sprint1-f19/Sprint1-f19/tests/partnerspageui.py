from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class PartnersPageUi:
    ## URL
    URL = 'https://uno-cpi-dev.herokuapp.com/'

    ##locators for  Maps
    Partners_Homepagelink = (By.XPATH, '//*[@id="target"]/ul/li[3]/a')
    Partners_Registercommunitypartnerlink = (By.XPATH, '//*[@id="myButton"]')
    Partners_Registercampuspartnerlink = (By.XPATH, '//*[@id="myButton1"]')
    searchfield_checkcommunitypartner = (By.XPATH, '//*[@id="partner_name"]')
    searchbutton_checkcommunitypartner = (By.XPATH, '//*[@id="next"]')
    registercommunitypartner_checkcommunitypartner = (By.XPATH, '//*[@id="lnk-register_partner"]')

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

    def partners_communitypartnerregister(self):
        Partners_Communitypartnerregister = self.browser.find_element(*self.Partners_Registercommunitypartnerlink)
        Partners_Communitypartnerregister.click()

    def partners_campuspartnerregister(self):
        Partners_Legislativedistrict = self.browser.find_element(*self.Partners_Registercampuspartnerlink)
        Partners_Legislativedistrict.click()

    def search_checkcommunitypartner(self):
        searchfield_checkcommunitypartner = self.browser.find_element(*self.searchfield_checkcommunitypartner)
        searchfield_checkcommunitypartner.click()



