import time

import pytest
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@pytest.fixture(scope='function')
def browser():
    manager = ChromeDriverManager()
    path = manager.install()

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"

    driver = Chrome(desired_capabilities=caps, executable_path=path)

    driver.get('https://target.my.com/')

    # Нажать войти
    wait = WebDriverWait(driver, 10)
    enter_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.responseHead-module-button-2yl51i"))
    )
    enter_button.click()

    # Ввести почту
    driver.find_element(By.NAME, "email").click()
    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "email").send_keys('awesome.uniq@yandex.ru')
    # Ввести пароль
    driver.find_element(By.NAME, "password").click()
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys('Default_password_1')
    # Подтвердить вход
    driver.find_element(By.CSS_SELECTOR, "div.authForm-module-button-1u2DYF").click()
    time.sleep(2)
    assert driver.current_url != "https://target.my.com/", "URL не изменился после логина"

    driver.maximize_window()

    yield driver

    # Закрыть браузер
    driver.quit()