from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ReportsPageUi:

    ## URL
    URL = 'https://uno-cpi-dev.herokuapp.com/'

    # Locators for Login
    Reports_missionarealink = (By.XPATH, '//*[@id="target"]/ul/li[2]/a')
    Reports_engagementtypelink = (By.XPATH, '//*[@id="target"]/ul/li[2]/ul/li[1]/ul/a[2]')
    Reports_communitypartnerlink = (By.XPATH, '//*[@id="target"]/ul/li[2]/ul/li[1]/ul/a[3]')
    Reports_projectslink = (By.XPATH, '//*[@id="target"]/ul/li[2]/ul/li[1]/ul/a[4]')
    Reports_asserttitlelink = (By.XPATH, '/html/body/div/div[2]/div/div/div[1]/div/label/b/h4')


    ### Initializer

    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods

    def load(self):
        self.browser.get(self.URL)

    #Mission Area link in dropdown of Reports link
    def reports_missionarea(self):
        Reports_MissionArea = self.browser.find_element(*self.Reports_missionarealink)
        Reports_MissionArea.click()

    def reports_engagementtype(self):
        Reports_Engagementtype = self.browser.find_element(*self.Reports_engagementtypelink)
        Reports_Engagementtype.click()

    def reports_projects(self):
        Reports_Projects = self.browser.find_element(*self.Reports_projectslink)
        Reports_Projects.click()

    def reports_assertreportname(self):
        reports_asserttitle = self.browser.find_element(*self.Reports_asserttitlelink)
        return reports_asserttitle.get_attribute('text')
