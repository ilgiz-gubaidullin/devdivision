from selenium.webdriver.common.by import By
from homework4.pages.segments_page import SegmentPage
from homework4.pages.base_page import BasePage
from homework4.helpers.locators import MainPageLocators
from homework4.pages.campaign_page import CampaignPage


class MainPage(BasePage):
    def open_campaign_page(self):
        return CampaignPage(self.driver)

    def open_segments_page(self):
        self._click(By.CSS_SELECTOR, MainPageLocators.SEGMENT_ICON)
        return SegmentPage(self.driver)
