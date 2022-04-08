from selenium.webdriver.common.by import By
from homework4.pages.base_page import BasePage


class LoginPage(BasePage):
    def start_auth(self):
        self._click(By.CSS_SELECTOR, "div.responseHead-module-button-2yl51i")

    def send_email(self, email):
        self._send_keys(By.CSS_SELECTOR, "[name='email']", email)

    def send_password(self, password):
        self._send_keys(By.CSS_SELECTOR, "[name='password']", password)

    def submit(self):
        self._click(By.CSS_SELECTOR, "div.authForm-module-button-1u2DYF")