from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    def _find_element(self, by, locator) -> WebElement:
        return self.driver.find_element(by, locator)

    def _click(self, by, locator):
        self.wait.until(EC.visibility_of_element_located((by, locator)))
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
        # return self._driver.execute_script('arguments[0].scrollIntoView({inline: "nearest"})', element)

    def _get_page_url(self):
        return self.driver.current_url

    def _get_attribute(self, by, locator, attribute):
        element = self._find_element(by, locator)
        element_attribute = element.get_attribute(attribute)
        return element_attribute
