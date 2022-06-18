from selenium.webdriver.common.by import By
from final_project.UI.pages.base_page import BasePage
from selenium.webdriver import ActionChains


class MainPage(BasePage):
    def open_main_page_link(self, locator):
        self._click(By.CSS_SELECTOR, locator)

    def move_cursor(self, locator):
        hover_element = self._find_element(By.CSS_SELECTOR, locator)
        return hover_element
        # ActionChains(self).move_to_element(hover_element).perform()

 # Поместите элементы, над которыми нужно навести курсор
# hover_element = driver.find_element_by_css_selector('div.list-top-mld p')
 # Выполните операцию наведения на элемент
# ActionChains(driver).move_to_element(hover_element).perform()