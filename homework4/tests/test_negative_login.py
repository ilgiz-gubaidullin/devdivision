import allure
import pytest
from homework4.pages.login_page import LoginPage
from homework4.helpers.credentials import UserData


@allure.story("Проверяем варианты негативного логина")
@allure.description("Тест проверяет 4 варианта негативного логина")
@pytest.mark.parametrize('email, password', (('wrong_email', 'wrong_pass'),
                                             (UserData.EMAIL, 'wrong_pass'),
                                             ('wrong_email', UserData.PASSWORD),
                                             ('', '')))
def test_negative_login(browser, email, password):
    with allure.step("Процесс логина"):
        page = LoginPage(browser)
        page.login(email, password)
    with allure.step("Проверка изменения URL"):
        assert browser.current_url != "https://target.my.com/dashboard", 'URL изменился на правильный после логина'
