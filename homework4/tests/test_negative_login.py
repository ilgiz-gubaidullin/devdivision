import time
import allure
import pytest
from selenium.webdriver import Chrome, ChromeOptions, Proxy, Remote
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from homework4.pages.login_page import LoginPage

correct_email = 'awesome.uniq@yandex.ru'
correct_password = 'Default_password_1'


@allure.story("Проверяем варианты негативного логина")
@pytest.mark.parametrize('email, password', (('wrong_email', 'wrong_pass'),
                                             (correct_email, 'wrong_pass'),
                                             ('wrong_email', correct_password),
                                             ('', '')))
def test_negative_login(email, password):
    """
    Тест проверяет 4 варианта негативного логина:
    1: неправильный email, неправильный пароль
    2: правильный email, неправильный пароль
    3: неправильный email, правильный пароль
    4: без email, без пароля
    """
    # manager = ChromeDriverManager()
    # path = manager.install()
    #
    # caps = DesiredCapabilities().CHROME
    # caps["pageLoadStrategy"] = "eager"
    #
    # driver = Chrome(desired_capabilities=caps, executable_path=path)

    capabilities = {
        "browserName": "chrome",
        "version": "89.0_vnc",
        "enableVNC": True,
        "pageLoadStrategy": "eager"
    }

    driver = Remote(
        "http://127.0.0.1:4444/wd/hub",
        options=ChromeOptions(),
        desired_capabilities=capabilities)

    driver.maximize_window()

    with allure.step("Заходим на сайт"):
        driver.get('https://target.my.com/')

    with allure.step("Процесс логина"):
        page = LoginPage(driver)
        page.start_auth()
        page.send_email(email)
        page.send_password(password)
        page.submit()

    time.sleep(3)

    with allure.step("Проверка изменения URL"):
        assert driver.current_url != "https://target.my.com/dashboard", 'URL изменился на правильный после логина'

    driver.quit()
