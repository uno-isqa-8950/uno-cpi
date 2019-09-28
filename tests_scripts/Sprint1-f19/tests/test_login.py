import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys


class TestLogin():
    @pytest.fixture
    def browser(self):
        global driver
        global username
        global password
        # Initialize ChromeDriver
        driver = Chrome()
        # maximize the browser window
        driver.maximize_window()
         # Wait implicitly for elements to be ready before attempting interactions
        driver.implicitly_wait(10)
        username = "aanzalone@unomaha.edu"
        password = "Capstone2019"
        # Set up some test case data
        URL = 'https://uno-cpi-dev.herokuapp.com/'
        # Navigate to the uno-cpi home page
        driver.get(URL)
        # In the DOM, it has an 'id' attribute of 'uno' for header
        search_header = driver.find_element_by_id('uno')
        PHRASE = 'University of Nebraska OmahaCommunity Partnership Initiative'
        assert search_header.get_attribute('text') == PHRASE
    # browser teardown
        yield
        driver.close()
        driver.quit()

    def test_login(self,browser):

        #Click on login icon
        login_icon = driver.find_element_by_xpath("//*[@id='target']/ul/li[4]/a")
        login_icon.click()
        # enter email id in email id field
        username_field = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div[2]/form/input[2]')
        username_field.send_keys(username)
        # enter password in password field
        password_field = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div[2]/form/input[3]')
        password_field.send_keys(password)
        #click on login button
        login_button = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div[2]/form/div[1]/p/button/i')
        login_button.click()
        # for assertion to login using toggle down
        toggle_down = driver.find_element_by_xpath('//*[@id="target"]/ul/li[6]/a')
        assert toggle_down.get_attribute('data-target') == "dropdown_target"

class TestLogout():
    def logout(self,browser):
        logout_dropdown = driver.find_element_by_xpath('//*[@id="target"]/ul/li[6]/a').click()
        logout_click = driver.find_element_by_xpath('//*[@id="target"]/ul/li[6]/div/a').click()
        successful_logout = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/h4')
        assert successful_logout.get_attribute('text') == "Logged Out"