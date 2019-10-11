from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class LoginPageUi:

    ## URL
    URL = 'https://uno-cpi-dev.herokuapp.com/'

    # Locators for Login
    Login_link = (By.XPATH, '//*[@id="target"]/ul/li[4]/a')
    Username_field = (By.XPATH, '/html/body/div/div/div/div/div/div[2]/div[2]/form/input[2]')
    Password_field = (By.XPATH, '/html/body/div/div/div/div/div/div[2]/div[2]/form/input[3]')
    Login_button = (By.XPATH, '/html/body/div/div/div/div/div/div[2]/div[2]/form/div[1]/p/button')
    Login_asserttoggle = (By.XPATH, '//*[@id="target"]/ul/li[6]/a')

    ## Locators for Logout
    Logout_dropdown = (By.XPATH, '//*[@id="target"]/ul/li[6]/a')
    Logout_click = (By.XPATH, '//*[@id="target"]/ul/li[6]/div/a')
    Successful_logout = (By.XPATH,'/html/body/div/div/div/div[1]/h4')

    # Initializer

    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods

    def load(self):
        self.browser.get(self.URL)
## login link on home page
    def login_link_click(self):
        login_link = self.browser.find_element(*self.Login_link)
        login_link.click()
## username field
    def login_username(self,username):
        login_username = self.browser.find_element(*self.Username_field)
        login_username.send_keys(username + Keys.RETURN)

## password field
    def login_password(self, password):
        login_password = self.browser.find_element(*self.Password_field)
        login_password.send_keys(password + Keys.RETURN)

## Login Button
    def login_button(self):
        login_button = self.browser.find_element(*self.Login_button)
        login_button.click()

## Login assertion
    def login_assertion(self):
        login_assert = self.browser.find_element(*self.Login_asserttoggle)
        value = login_assert.get_attribute('class')
        return value
## Logout dropdown

    def logout_dropdown(self):
        logout_dropdown = self.browser.find_element(*self.Logout_dropdown)
        logout_dropdown.click()

## Logout Click
    def logout_click(self):
        logout_click = self.browser.find_element(*self.Login_button)
        logout_click.click()

## Logout Assertion
    def logout_assertion(self):
        successful_logout = self.browser.find_element(*self.Successful_logout)
        success = successful_logout.get_attribute('text') ##Logged Out
        return success



