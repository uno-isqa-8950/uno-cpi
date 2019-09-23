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

    def test_mapslinks(self,browser):
        global maps_link
        global page_title
        # test for community partners maps
        maps_link = driver.find_element_by_xpath('//*[@id="target"]/ul/li[1]/a')
        maps_link.click()
        driver.implicitly_wait(50)
        maps_link.click()
        communitypartners_maps = driver.find_element_by_xpath('//*[@id="target"]/ul/li[1]/div/a[1]').click()
        driver.implicitly_wait(200)
        page_sidebar = driver.find_element_by_xpath('//*[@id="sidebarCollapse"]')
        driver.implicitly_wait(30)
        assert page_sidebar.get_attribute('id') == "sidebarCollapse"
        #test for legislative districts maps
        maps_link.click()
        driver.implicitly_wait(50)
        maps_link.click()
        legislativedistricts_maps = driver.find_element_by_xpath('//*[@id="target"]/ul/li[1]/div/a[2]').click()
        driver.implicitly_wait(100)
        assert page_title.get_attribute('id') == "Maps: Legislative Districts"