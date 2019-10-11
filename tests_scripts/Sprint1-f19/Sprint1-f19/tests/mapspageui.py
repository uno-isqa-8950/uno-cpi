from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class MapsPageUi:

    ## URL
    URL = 'https://uno-cpi-dev.herokuapp.com/'

    ##locators for  Maps
    Maps_Homepagelink = (By.XPATH, '//*[@id="target"]/ul/li[1]/a')
    Maps_Communitypartnerslink = (By.XPATH, '//*[@id="target"]/ul/li[1]/div/a[1]')
    Maps_asserttitlelink = (By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div[2]/div/label/b')
    Maps_legislativedistrictlink = (By.XPATH, '//*[@id="target"]/ul/li[1]/div/a[2]')
    Maps_communitypartnertypelink = (By.XPATH, '//*[@id="target"]/ul/li[1]/div/a[3]')
    Maps_projectslink = (By.XPATH, '//*[@id="target"]/ul/li[1]/div/a[4]')



    ### Initializer

    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods

    def load(self):
        self.browser.get(self.URL)
    ##maps link on home page

    def maps_homepage(self):
        Maps_Homepage = self.browser.find_element(*self.Maps_Homepagelink)
        Maps_Homepage.click()

    def maps_communitypartners(self):
        Maps_Communitypartners = self.browser.find_element(*self.Maps_Communitypartnerslink)
        Maps_Communitypartners.click()

    def maps_assertmapname(self):
        maps_asserttitle = self.browser.find_element(*self.Maps_asserttitlelink)
        return maps_asserttitle.get_attribute('text')

    def maps_legislativedistrict(self):
        Maps_Legislativedistrict = self.browser.find_element(*self.Maps_legislativedistrictlink)
        Maps_Legislativedistrict.click()

    def maps_communitypartnertype(self):
        Maps_CommunityPartnerType = self.browser.find_element(*self.Maps_communitypartnertypelink)
        Maps_CommunityPartnerType.click()

    def maps_project(self):
        Maps_Project = self.browser.find_element(*self.Maps_projectslink)
        Maps_Project.click()