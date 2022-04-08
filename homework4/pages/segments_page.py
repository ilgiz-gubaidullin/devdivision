import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from homework4.pages.base_page import BasePage
from datetime import datetime


time_title = datetime.now().strftime('%H.%M.%S-%d.%m.%Y')
segment_name = "Auto segment name " + time_title


class SegmentPage(BasePage):
    def add_segment(self):
        try:
            self._click(By.CSS_SELECTOR, '[href="/segments/segments_list/new/"]')
        except TimeoutException:
            self._click(By.CSS_SELECTOR, '.button__text')

        time.sleep(2)

        self._click(By.CSS_SELECTOR, '.adding-segments-source__checkbox ')
        self._click(By.CSS_SELECTOR, '.adding-segments-modal__btn-wrap  > .button.button_submit  > .button__text')

        self._send_keys(By.CSS_SELECTOR, '.input_create-segment-form .input__wrap > input.input__inp', segment_name)
        self._click(By.CSS_SELECTOR, '.create-segment-form__btn-wrap  > .button > .button__text')

    def check_segment_exist(self):
        assert segment_name == self._get_text(By.CSS_SELECTOR, f'[title="{segment_name}"]')

    def delete_segments(self):
        self._click(By.CSS_SELECTOR, '.segmentsTable-module-idHeaderCellWrap-1M1sHd > .input-module-input-1Uxo5D')
        self._click(By.CSS_SELECTOR, '.select-module-arrow-3cxrfd')
        self._click(By.CSS_SELECTOR, '[title="Удалить"]')

    def check_deletion(self):
        attribute = self._get_attribute(By.CSS_SELECTOR, '.page_segments__instruction-wrap.js-instruction-wrap', 'style')
        assert attribute == 'display: block;'
