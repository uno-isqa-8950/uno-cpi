from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ProjectsPageUi:

    ## URL
    URL = 'https://uno-cpi-dev.herokuapp.com/'

    # Locators for Projects
    Projects_link = (By.XPATH, '//*[@id="target"]/ul/li[3]/a')
    Projects_allprojectslink = (By.XPATH, '//*[@id="target"]/ul/li[3]/div/a[1]')
    Projects_myprojectslink = (By.XPATH, '//*[@id="target"]/ul/li[3]/div/a[2]')
    Projects_checkprojectlink = (By.XPATH, '//*[@id="target"]/ul/li[3]/div/a[3]')
    Projects_mydraftslink = (By.XPATH, '//*[@id="target"]/ul/li[3]/div/a[4]')
    Checkproject_projectnamefield = (By.XPATH, '//*[@id="projectName"]')
    Checkproject__communitytypesfield =''
    Checkproject_campustypesfield = ''
    Checkproject_searchbutton = (By.XPATH, '//*[@id="streambutton"]')
    checkproject_createbutton = (By.XPATH, '//*[@id="lnk-create_project"]')


    ### Initializer

    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods

    def load(self):
        self.browser.get(self.URL)

    #Projects Link on home page
    def projects_homepage(self):
        Projects_Homepage = self.browser.find_element(*self.Projects_link)
        Projects_Homepage.click()

    def allprojects_projects(self):
        allprojects_projects = self.browser.find_element(*self.Projects_allprojectslink)
        allprojects_projects.click()

    def myprojects_projects(self):
        myprojects_projects = self.browser.find_element(*self.Projects_myprojectslink)
        myprojects_projects.click()

    def checkproject_projects(self):
        checkproject_projects = self.browser.find_element(*self.Projects_checkprojectlink)
        checkproject_projects.click()

    def mydrafts_projects(self):
        mydrafts_projects = self.browser.find_element(*self.Projects_mydraftslink)
        mydrafts_projects.click()

    def projectname_checkproject(self, projectname):
        projectname_checkproject = self.browser.find_element(*self.Checkproject_projectnamefield)
        projectname_checkproject.send_keys(projectname + Keys.RETURN)

    def searchbutton_checkproject(self, searchbutton):
        searchbutton_checkproject = self.browser.find_element(*self.Checkproject_projectnamefield)
        searchbutton_checkproject.click()

    def createproject_checkproject(self):
        createproject_checkproject = self.browser.find_element(*self.checkproject_createbutton)
        createproject_checkproject.click()







