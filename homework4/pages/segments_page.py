import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from homework4.pages.base_page import BasePage
from homework4.helpers.locators import SegmentsPageLocators


class SegmentPage(BasePage):
    def add_segment(self, new_segment_name):
        try:
            self._click(By.CSS_SELECTOR, SegmentsPageLocators.CREATE_LINK)
        except TimeoutException:
            self._click(By.CSS_SELECTOR, SegmentsPageLocators.CREATE_SEGMENT_BUTTON)

        self._click(By.CSS_SELECTOR, SegmentsPageLocators.CHECKBOX_PLAYED)
        self._click(By.CSS_SELECTOR, SegmentsPageLocators.ADD_SEGMENT_BUTTON)
        self._send_keys(By.CSS_SELECTOR, SegmentsPageLocators.SEGMENT_NAME, new_segment_name)
        self._click(By.CSS_SELECTOR, SegmentsPageLocators.CREATE_SUBMIT_BUTTON)

    def check_segment_exist(self, segment_name):
        assert segment_name == self._get_text(By.CSS_SELECTOR, f'[title="{segment_name}"]')

    def delete_segment(self, segment_name):
        segment_link = self._get_attribute(By.XPATH, f"//*[text() = '{segment_name}']", "href")
        segment_id = segment_link.split('/')[-1]
        self._click(By.XPATH, f'//div[@data-test="remove-{segment_id} row-{segment_id}"]/span')
        self._click(By.CSS_SELECTOR, SegmentsPageLocators.DELETE_SUBMIT_BUTTON)

    def check_deletion(self, segment_name):
        with pytest.raises(TimeoutException):
            self._find_elements(By.CSS_SELECTOR, f'[title="{segment_name}"]')
            pytest.fail("Deleted test not found")
