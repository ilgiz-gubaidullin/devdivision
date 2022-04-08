from selenium.webdriver.common.by import By

from homework4.pages.base_page import BasePage


class MainPage(BasePage):
    def open_campaign_page(self):
        self._click(By.CSS_SELECTOR, '[href="/campaign/new"]')

    def open_segments_page(self):
        self._click(By.CSS_SELECTOR, '[href="/segments"]')