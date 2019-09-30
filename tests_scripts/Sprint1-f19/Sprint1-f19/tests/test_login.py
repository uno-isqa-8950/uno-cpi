from .loginpageui import LoginPageUi

def test_basic_login(browser):
    login_page = LoginPageUi(browser)
    # Given the  home page is displayed
    login_page.load()
    #browser.implicitly_wait(10)
    USERNAME = 'aanzalone@unomaha.edu'
    PASSWORD = 'Capstone2019'
    # When the user clicks on login link
    login_page.login_link_click()
    login_page.login_username(USERNAME)
    login_page.login_password(PASSWORD)
    #login_page.login_button()

    # After logging in assert the drown down button
    assert 'nav-link dropdown-toggle' in login_page.login_assertion()



