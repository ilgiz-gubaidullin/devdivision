import time
import pytest
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from homework4.pages.login_page import LoginPage

correct_email = 'awesome.uniq@yandex.ru'
correct_password = 'Default_password_1'


@pytest.mark.parametrize('email, password', (('wrong_email', 'wrong_pass'),
                                             (correct_email, 'wrong_pass'),
                                             ('wrong_email', correct_password),
                                             ('', '')))
def test_negative_login(email, password):
    manager = ChromeDriverManager()
    path = manager.install()

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"

    driver = Chrome(desired_capabilities=caps, executable_path=path)

    driver.get('https://target.my.com/')

    page = LoginPage(driver)

    page.start_auth()
    page.send_email(email)
    page.send_password(password)
    page.submit()

    time.sleep(3)

    assert driver.current_url != "https://target.my.com/dashboard", 'URL изменился на правильный после логина'
    driver.quit()
