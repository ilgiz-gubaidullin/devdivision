from selenium.webdriver.common.by import By
from homework4.pages.base_page import BasePage
from homework4.helpers.locators import LoginPageLocators


class LoginPage(BasePage):
    def login(self, email, password):
        self._click(By.XPATH, LoginPageLocators.ENTER_BUTTON)
        self._send_keys(By.CSS_SELECTOR, LoginPageLocators.EMAIL_INPUT, email)
        self._send_keys(By.CSS_SELECTOR, LoginPageLocators.PASSWORD_INPUT, password)
        self._click(By.CSS_SELECTOR, LoginPageLocators.SUBMIT)
