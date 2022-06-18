import pytest
from final_project.UI.ui_base import BaseUISuiteTest
import allure
from final_project.UI.pages.login_page import LoginPage
from final_project.helpers.site_data import SiteData, MainPageLinks
from final_project.helpers.locators import MainPageLocators
from selenium.webdriver import ActionChains


class TestMainPageUI(BaseUISuiteTest):

    @pytest.mark.parametrize('username, password', (('wrong_username', 'wrong_pass'),
                                                    (SiteData.main_user, 'wrong_pass'),
                                                    ('wrong_username', SiteData.main_user_pass),
                                                    ('', '')))
    def test_negative_login(self, browser_final, username, password):
        with allure.step("Процесс логина"):
            page = LoginPage(browser_final)
            page.login(username, password)
        with allure.step("Проверка логина пользователя"):
            assert browser_final.current_url != f"{SiteData.url}/welcome", 'URL не должен меняться на успешный'

    def test_login_success(self, browser_final):
        with allure.step("Процесс логина"):
            page = LoginPage(browser_final)
            page.login(SiteData.main_user, SiteData.main_user_pass)
        with allure.step("Проверка логина пользователя"):
            page.check_user_logged(SiteData.main_user)
            assert browser_final.current_url == f"{SiteData.url}welcome/", 'URL должен меняться на успешный'

    @pytest.mark.parametrize('link_locator', [MainPageLocators.WHAT_IS_API_ICON,
                                              MainPageLocators.INTERNET_FUTURE_ICON,
                                              MainPageLocators.SMTP_ICON])
    def test_links_main_page_container(self, browser_final, main_page_fixture_final, link_locator):
        page = main_page_fixture_final
        page.open_main_page_link(link_locator)
        browser_final.switch_to.window(browser_final.window_handles[1])
        assert browser_final.current_url in MainPageLinks.container_links

    @pytest.mark.parametrize('hover_element, link_locator', ((MainPageLocators.PYTHON_HOVER, MainPageLocators.PYTHON_HISTORY),
                                                             (MainPageLocators.PYTHON_HOVER, MainPageLocators.FLASK)))
    def test_links_main_page_header(self, browser_final, main_page_fixture_final, hover_element, link_locator):
        page = main_page_fixture_final
        element = page.move_cursor(hover_element)
        ActionChains(browser_final).move_to_element(element).perform()

        page.open_main_page_link(link_locator)
        browser_final.switch_to.window(browser_final.window_handles[1])
        assert browser_final.current_url in MainPageLinks.header_links

