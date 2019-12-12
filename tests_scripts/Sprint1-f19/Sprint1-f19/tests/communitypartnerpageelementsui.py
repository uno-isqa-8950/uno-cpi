from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class PartnersPageUi:
    ## URL
    URL = 'https://uno-cpi-dev.herokuapp.com/'

    ##locators for  Maps
    Partners_Homepagelink = (By.XPATH, '//*[@id="target"]/ul/li[3]/a')
    Partners_Registercommunitypartnerlink = (By.XPATH, '//*[@id="myButton"]')
    Partners_checkcommunitypartnertext = (By.XPATH, '//*[@id="partner_name"]')
    Partners_checkcommunitysearchbutton = (By.XPATH, '//*[@id="next"]')
    Partners_createcommunitybutton = (By.XPATH, '//*[@id="lnk-register_partner"]')
    Partners_communityacronym = (By.XPATH, '//*[@id="id_acronym"]')
    Partners_communitypartnertype = (By.XPATH, '//*[@id="select2-id_community_type-container"]')
    Partners_communitywebsite = (By.XPATH, '//*[@id="id_website_url"]')
    Partners_communityaddresschoice = (By.XPATH, '//*[@id="id_online_only"]')
    Partners_communityaddresstab = (By.XPATH, '//*[@id="form-step-0"]/div[5]/button')
    Partners_communityaddressline1 = (By.XPATH, '//*[@id="id_address_line1"]')
    Partners_communitycity = (By.XPATH, '//*[@id="id_city"]')
    Partners_communitycountry = (By.XPATH, '//*[@id="id_country"]')
    Partners_communitystate = (By.XPATH, '//*[@id="id_state"]')
    Partners_communityzip = (By.XPATH, '//*[@id="id_zip"]')
    Partners_communitynextpage = (By.XPATH, '//*[@id="smartwizard"]/div[2]/div/button[2]')
    Partners_communityfocusarea = (By.XPATH, '//*[@id="id_primary_mission-0-mission_area"]/option[2]')
    Partners_communityotherfocusarea = (By.XPATH, '//*[@id="id_mission-0-mission_area"]/option[2]')
    Partners_addcommunityfocus = (By.XPATH, '//*[@id="step-2"]/div[2]/div[2]/div/div[2]/div/i')
    Partners_communityterms = (By.XPATH, '//*[@id="terms"]')
    Partners_communitysubmit = (By.XPATH, '//*[@id="submit"]')

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

    def partners_checkcommunitypartnertext(self):
        Partners_Checkcommunitypartnertextt = self.browser.find_element(*self.Partners_checkcommunitypartnertext)
        Partners_Checkcommunitypartnertextt.send_keys("Testcreatecommu" + Keys.RETURN)

    def partners_checkcommunitysearchbutton(self):
        partners_checkcommunitysearchbutton = self.browser.find_element(*self.Partners_checkcommunitysearchbutton)
        partners_checkcommunitysearchbutton.click()

    def partners_createcommunitybutton(self):
        Partners_createcommunitybutton = self.browser.find_element(*self.Partners_createcommunitybutton)
        Partners_createcommunitybutton.click()

    def partners_communityacronym(self):
        Partners_communityacronym = self.browser.find_element(*self.Partners_communityacronym)
        Partners_communityacronym.send_keys("TEST" + Keys.RETURN)

    def partners_communitypartnertype(self):
        Partners_communitypartnertype = self.browser.find_element(*self.Partners_communitypartnertype)
        Partners_communitypartnertype.click()

    def partners_communitywebsite(self):
        Partners_communitywebsite = self.browser.find_element(*self.Partners_communitywebsite)
        Partners_communitywebsite.click()

    def partners_communityaddresschoice(self):
        Partners_communityaddresschoice = self.browser.find_element(*self.Partners_communityaddresschoice)
        Partners_communityaddresschoice.click()

    def partners_communityaddresstab(self):
        Partners_communityaddresstab = self.browser.find_element(*self.Partners_communityaddresstab)
        Partners_communityaddresstab.click()

    def partners_communitynextpage(self):
        Partners_communitynextpage = self.browser.find_element(*self.Partners_communitynextpage)
        Partners_communitynextpage.click()

    def partners_communityfocusarea(self):
        Partners_communityfocusarea = self.browser.find_element(*self.Partners_communityfocusarea)
        Partners_communityfocusarea.click()

    def partners_communityotherfocusarea(self):
        Partners_communityotherfocusarea = self.browser.find_element(*self.Partners_communityotherfocusarea)
        Partners_communityotherfocusarea.click()

    def partners_addcommunityfocus(self):
        Partners_addcommunityfocus = self.browser.find_element(*self.Partners_addcommunityfocus)
        Partners_addcommunityfocus.click()

    def partners_communityterms(self):
        Partners_communityterms = self.browser.find_element(*self.Partners_communityterms)
        Partners_communityterms.click()

    def partners_communitysubmit(self):
        Partners_communitysubmit = self.browser.find_element(*self.Partners_communitysubmit)
        Partners_communitysubmit.click()

