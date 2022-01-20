from autopost import browser


def test_login_page():
    home_page = HomePage(browser)
    login_page = home_page.go_to_login_page()
    login_page.login("username", "password")

    errors = browser.find_elements_by_css_selector('#error_message')
    assert len(errors) == 0

if __name__ == '__main__':
    test_login_page()
