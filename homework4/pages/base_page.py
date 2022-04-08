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