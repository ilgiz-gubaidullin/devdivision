import time
from datetime import datetime
from selenium.webdriver.common.by import By
from homework4.pages.base_page import BasePage

time_title = datetime.now().strftime('%H.%M.%S-%d.%m.%Y')
campaign_name = "Auto campaign name " + time_title


class CampaignPage(BasePage):
    def fill_data(self):
        self._click(By.CSS_SELECTOR, '.button-module-button-1v2gG_.button-module-blue-3nuTZJ.button-module-button-1v2gG_[data-test="button"] > .button-module-textWrapper-22z69-')
        self._click(By.CSS_SELECTOR, '[cid="view605"]')

        self._send_keys(By.CSS_SELECTOR, '[data-gtm-id="ad_url_text"]', "https://target.my.com/")
        time.sleep(3)

        self._send_keys(By.CSS_SELECTOR, '.input.input_campaign-name.input_with-close > .input__wrap > .input__inp.js-form-element', campaign_name)

        self._send_keys(By.CSS_SELECTOR, '[data-test="budget-per_day"]', "100")
        self._send_keys(By.CSS_SELECTOR, '[data-test="budget-total"]', "100")

        self._click(By.CSS_SELECTOR, '#patterns_banner_4')
        time.sleep(3)

    def upload_file(self, upload_file_path):
        self._send_keys_to_upload(By.CSS_SELECTOR, '.roles-module-uploadButton-ZO1MPT .button-module-textWrapper-22z69-', upload_file_path)
        time.sleep(3)
        self._click(By.CSS_SELECTOR, '.image-cropper__save.js-save')
        time.sleep(3)
        self._click(By.CSS_SELECTOR, '[cid="view553"]')




