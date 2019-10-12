from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ChartsPageUi:

    ## URL
    URL = 'https://uno-cpi-dev.herokuapp.com/'

    # Locators for Login
    Charts_missionarealink = (By.XPATH, '//*[@id="target"]/ul/li[2]/ul/li[2]/ul/a[1]')
    Charts_engagementtypelink = (By.XPATH, '//*[@id="target"]/ul/li[2]/ul/li[2]/ul/a[2]')
    Charts_asserttitlelink = (By.XPATH, '/html/body/div/div[2]/div/div/div[1]/div/label/b/h4')


    ### Initializer

    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods

    def load(self):
        self.browser.get(self.URL)

    #Mission Area link in dropdown of Charts link
    def charts_missionarea(self):
        charts_MissionArea = self.browser.find_element(*self.Charts_missionarealink)
        charts_MissionArea.click()

    def charts_engagementtype(self):
        charts_Engagementtype = self.browser.find_element(*self.Charts_engagementtypelink)
        charts_Engagementtype.click()

    def charts_assertchartname(self):
        charts_asserttitle = self.browser.find_element(*self.Charts_asserttitlelink)
        return charts_asserttitle.get_attribute('text')