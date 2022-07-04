from selenium.webdriver.common.by import By
from final_project.UI.pages.base_page import BasePage
from final_project.helpers.locators import RegPageLocators


class RegPage(BasePage):
    def create_account(self, user_data, checkbox=True):
        self._send_keys(By.CSS_SELECTOR, RegPageLocators.NAME, user_data["name"])
        self._send_keys(By.CSS_SELECTOR, RegPageLocators.SURNAME, user_data["surname"])
        self._send_keys(By.CSS_SELECTOR, RegPageLocators.MIDDLENAME, user_data["middle_name"])
        self._send_keys(By.CSS_SELECTOR, RegPageLocators.USERNAME, user_data["username"])
        self._send_keys(By.CSS_SELECTOR, RegPageLocators.EMAIL, user_data["email"])
        self._send_keys(By.CSS_SELECTOR, RegPageLocators.PASSWORD, user_data["password"])
        self._send_keys(By.CSS_SELECTOR, RegPageLocators.REPEAT_PASSWORD, user_data["password"])
        if checkbox:
            self._click(By.CSS_SELECTOR, RegPageLocators.SDET_CHECKBOX)
        self._click(By.CSS_SELECTOR, RegPageLocators.SUBMIT)
