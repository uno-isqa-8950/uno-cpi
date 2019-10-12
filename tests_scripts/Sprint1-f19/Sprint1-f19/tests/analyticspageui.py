from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class AnalyticsPageUi:

    ## URL
    URL = 'https://uno-cpi-dev.herokuapp.com/'

    # Locators for Login
    Analytics_link = (By.XPATH, '//*[@id="target"]/ul/li[2]/a')
    Analytics_reportslink = (By.XPATH, '//*[@id="target"]/ul/li[2]/ul/li[1]/a')
    Analytics_chartslink = (By.XPATH, '//*[@id="target"]/ul/li[2]/ul/li[2]/a')


    ### Initializer

    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods

    def load(self):
        self.browser.get(self.URL)

    #Analytics Link on home page
    def analytics_homepage(self):
        Analytics_Homepage = self.browser.find_element(*self.Analytics_link)
        Analytics_Homepage.click()

    def reports_analytics(self):
        Reports_Analytics = self.browser.find_element(*self.Analytics_reportslink)
        Reports_Analytics.click()

    def charts_analytics(self):
        Charts_Analytics = self.browser.find_element(*self.Analytics_chartslink)
        Charts_Analytics.click()
