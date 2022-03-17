from datetime import datetime
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import names


@pytest.mark.UI
def test_edit_profile_info(browser):
    # Переход на страницу профиля
    browser.get('https://target.my.com/profile/contacts')
    wait = WebDriverWait(browser, 15)

    # Редактируем ФИО
    fio_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-name="fio"] > div > input'))
    )
    fio_button.click()
    fio_button.clear()
    fio_button.send_keys(datetime.now().strftime(names.get_full_name(gender='female')))

    # Редактируем телефон
    phone_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-name="phone"] > div > input'))
    )
    phone_button.click()
    phone_button.clear()
    phone_button.send_keys(datetime.now().strftime('%H.%M.%S'))

    # Нажать сохранить
    browser.find_element(By.CSS_SELECTOR, ".button.button_submit").click()

    # Проверяем, что появляется скрытое уведомление показываемое при успешном сохранении
    assert browser.find_element(By.CSS_SELECTOR, '.button.button_submit.button_pending').is_displayed()


@pytest.mark.UI
def test_logout(browser):
    # Нажать на личный кабинет
    time.sleep(6)
    browser.find_element(By.CSS_SELECTOR, ".right-module-rightButton-3e-duF").click()

    # Нажать выйти
    time.sleep(6)
    browser.find_element(By.CSS_SELECTOR, '[href="/logout"]').click()

    assert browser.current_url == "https://target.my.com/", "URL не соответствует разлогиненному"


@pytest.mark.UI
@pytest.mark.parametrize("button, url", (("[href='/profile']", 'https://target.my.com/profile/contacts'),
                                         ("[href='/segments']", 'https://target.my.com/segments/segments_list')))
def test_header_buttons(browser, button, url):
    # Нажать на кнопку в хедере
    time.sleep(7)
    browser.find_element(By.CSS_SELECTOR, button).click()

    time.sleep(3)
    assert browser.current_url == url, f'URL не соответствует нажатию кнопки {button}'
