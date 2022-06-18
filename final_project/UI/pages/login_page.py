from selenium.webdriver.common.by import By
from final_project.helpers.locators import LoginPageLocators
from final_project.helpers.locators import MainPageLocators
from final_project.UI.pages.base_page import BasePage


class LoginPage(BasePage):
    def login(self, email, password):
        self._send_keys(By.CSS_SELECTOR, LoginPageLocators.USERNAME_INPUT, email)
        self._send_keys(By.CSS_SELECTOR, LoginPageLocators.PASSWORD_INPUT, password)
        self._click(By.CSS_SELECTOR, LoginPageLocators.SUBMIT)

    def check_user_logged(self, username):
        assert f"Logged as {username}" == self._get_text(By.CSS_SELECTOR, MainPageLocators.LOGGED_NAME)

