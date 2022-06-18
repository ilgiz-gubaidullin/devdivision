from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15,
                                  ignored_exceptions=StaleElementReferenceException)

    def _find_element(self, by, locator) -> WebElement:
        self.wait.until(EC.presence_of_element_located((by, locator)))
        return self.driver.find_element(by, locator)

    def _find_elements(self, by, locator) -> List[WebElement]:
        self.wait.until(EC.presence_of_element_located((by, locator)))
        return self.driver.find_elements(by, locator)

    def _click(self, by, locator):
        self.wait.until(EC.visibility_of_element_located((by, locator)))
        self.wait.until(EC.element_to_be_clickable((by, locator)))
        self._find_element(by, locator).click()

    def _send_keys(self, by, locator, text):
        self.wait.until(EC.visibility_of_element_located((by, locator)))
        self._find_element(by, locator).clear()
        self._find_element(by, locator).send_keys(text)

    def _send_keys_to_upload(self, by, locator, text):
        self.wait.until(EC.presence_of_element_located((by, locator)))
        self._find_element(by, locator).send_keys(text)

    def _get_text(self, by, locator):
        self.wait.until(EC.visibility_of_element_located((by, locator)))
        element = self._find_element(by, locator)
        return element.text

    def _scroll_by_element(self, selector):
        return self.driver.execute_script(f"document.querySelector('{selector}').scrollIntoView()")

    def _get_page_url(self):
        return self.driver.current_url

    def _get_attribute(self, by, locator, attribute):
        element = self._find_element(by, locator)
        element_attribute = element.get_attribute(attribute)
        return element_attribute

