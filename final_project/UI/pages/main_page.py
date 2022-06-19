from selenium.webdriver.common.by import By
from final_project.UI.pages.base_page import BasePage
from final_project.helpers.locators import MainPageLocators


class MainPage(BasePage):
    def open_main_page_link(self, locator):
        self._click(By.CSS_SELECTOR, locator)

    def move_cursor(self, locator):
        hover_element = self._find_element(By.CSS_SELECTOR, locator)
        return hover_element

    def check_footer_str_present(self):
        text = self._get_text(By.CSS_SELECTOR, MainPageLocators.FOOTER_TEXT)
        assert text is not None and isinstance(text, str), "Текст пустой или не является строкой"

    def make_logout(self):
        self._click(By.CSS_SELECTOR, MainPageLocators.LOGOUT_BUTTON)

