import time
import pytest
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from homework4.pages.login_page import LoginPage
from homework4.pages.main_page import MainPage


@pytest.fixture(scope='function')
def browser():
    manager = ChromeDriverManager()
    path = manager.install()

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"

    driver = Chrome(desired_capabilities=caps, executable_path=path)

    driver.get('https://target.my.com/')

    page = LoginPage(driver)

    page.start_auth()
    page.send_email('awesome.uniq@yandex.ru')
    page.send_password('Default_password_1')
    page.submit()

    time.sleep(3)

    driver.maximize_window()

    page = MainPage(driver)

    yield page

    # Закрыть браузер
    driver.quit()
