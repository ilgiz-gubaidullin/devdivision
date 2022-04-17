from selenium.webdriver.common.by import By
from homework4.pages.base_page import BasePage
from homework4.helpers.locators import CampaignPageLocators


class CampaignPage(BasePage):
    def fill_data(self, new_campaign_name):
        self._click(By.XPATH, CampaignPageLocators.CREATE_CAMP_BUTTON)
        self._click(By.CSS_SELECTOR, CampaignPageLocators.TRAFFIC_BLOCK)
        self._send_keys(By.CSS_SELECTOR, CampaignPageLocators.CAMP_LINK, "https://target.my.com/")
        self._send_keys(By.CSS_SELECTOR, CampaignPageLocators.CAMP_NAME, new_campaign_name)
        self._send_keys(By.CSS_SELECTOR, CampaignPageLocators.DAY_BUDGET, "100")
        self._send_keys(By.CSS_SELECTOR, CampaignPageLocators.TOTAL_BUDGET, "100")
        self._click(By.CSS_SELECTOR, CampaignPageLocators.BANNER_BLOCK)

    def upload_file(self, upload_file_path):
        self._send_keys_to_upload(By.CSS_SELECTOR, CampaignPageLocators.IMAGE_INPUT, upload_file_path)
        self._click(By.CSS_SELECTOR, CampaignPageLocators.CROP_IMAGE_BUTTON)
        self._click(By.CSS_SELECTOR, CampaignPageLocators.SUBMIT_BUTTON)

    def check_campaign_created(self, campaign_name):
        assert campaign_name == self._get_text(By.CSS_SELECTOR, f'[title="{campaign_name}"]')