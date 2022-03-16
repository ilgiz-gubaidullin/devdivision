from datetime import datetime
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.UI
def test_edit_profile_info(browser):
    # Переход на страницу профиля
    browser.get('https://target.my.com/profile/contacts')

    time.sleep(5)

    # Редактируем ФИО
    browser.find_element(By.CSS_SELECTOR, '[data-name="fio"]').click()
    browser.find_element(By.CSS_SELECTOR, "[data-name='fio']").clear()
    browser.find_element(By.CSS_SELECTOR, "[data-name='fio']").send_keys(datetime.now().strftime('%H.%M.%S'))

    # Контактный телефон
    browser.find_element(By.CSS_SELECTOR, '[data-name="phone"]').click()
    browser.find_element(By.CSS_SELECTOR, '[data-name="phone"]').clear()
    browser.find_element(By.CSS_SELECTOR, '[data-name="phone"]').send_keys('123456789')

    # Нажать сохранить
    browser.find_element(By.CSS_SELECTOR, ".button.button_submit")


@pytest.mark.UI
def test_logout(browser):
    # Нажать на личный кабинет
    time.sleep(10)
    browser.find_element(By.CSS_SELECTOR, ".right-module-rightButton-3e-duF").click()

    # Нажать выйти
    time.sleep(10)
    browser.find_element(By.CSS_SELECTOR, '[href="/logout"]').click()

    assert browser.current_url == "https://target.my.com/", "URL не соответствует разлогиненному"


@pytest.mark.UI
@pytest.mark.parametrize("button, url", (('[href="/profile"]', 'https://target.my.com/profile/contacts'),('[href="/tools"]', 'https://target.my.com/tools/feeds')))
def test_header_buttons(browser, button, url):
    time.sleep(10)
    browser.find_element(By.CSS_SELECTOR, button).click()

    time.sleep(5)
    assert browser.current_url == url, f'URL не соответствует нажатию кнопки {button}'
