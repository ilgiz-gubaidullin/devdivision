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

    @pytest.mark.parametrize('username, password', ((SiteData.main_user, SiteData.main_user_pass),
                                                    (f"   {SiteData.main_user}   ", f"  {SiteData.main_user_pass}  ")))
    def test_login_success(self, browser_final, username, password):
        with allure.step("Процесс логина"):
            page = LoginPage(browser_final)
            page.login(username, password)
        with allure.step("Проверка логина пользователя"):
            assert browser_final.current_url == f"{SiteData.url}welcome/", 'URL должен меняться на успешный'
            page.check_user_logged(username)

    @pytest.mark.parametrize('link_locator', [MainPageLocators.WHAT_IS_API_ICON,
                                              MainPageLocators.INTERNET_FUTURE_ICON,
                                              MainPageLocators.SMTP_ICON])
    def test_links_main_page_container(self, browser_final, main_page_fixture_final, link_locator):
        page = main_page_fixture_final
        page.open_main_page_link(link_locator)
        browser_final.switch_to.window(browser_final.window_handles[1])
        assert browser_final.current_url in MainPageLinks.container_links

    @pytest.mark.parametrize('hover_element, link_locator', ((MainPageLocators.PYTHON_HOVER, MainPageLocators.PYTHON_HISTORY),
                                                             (MainPageLocators.PYTHON_HOVER, MainPageLocators.ABOUT_FLASK),
                                                             (MainPageLocators.LINUX_HOVER, MainPageLocators.DOWNLOAD_CENTOS),
                                                             (MainPageLocators.NETWORK_HOVER, MainPageLocators.WIRESHARK_NEWS),
                                                             (MainPageLocators.NETWORK_HOVER, MainPageLocators.WIRESHARK_DOWNLOAD),
                                                             (MainPageLocators.NETWORK_HOVER, MainPageLocators.TCDUMP_EXAMPLES),
                                                             ))
    def test_links_main_page_header(self, browser_final, main_page_fixture_final, hover_element, link_locator):
        page = main_page_fixture_final
        element = page.move_cursor(hover_element)
        ActionChains(browser_final).move_to_element(element).perform()
        page.open_main_page_link(link_locator)
        browser_final.switch_to.window(browser_final.window_handles[1])
        assert browser_final.current_url in MainPageLinks.header_links

    def test_footer_str_present(self, browser_final, main_page_fixture_final):
        page = main_page_fixture_final
        page.check_footer_str_present()

    def test_logout(self, browser_final, main_page_fixture_final):
        page = main_page_fixture_final
        page.make_logout()
        assert browser_final.current_url == f"{SiteData.url}login", 'URL не соответствует странице логина'

    @pytest.mark.parametrize('icon_locator', [MainPageLocators.TM_ICON,
                                              MainPageLocators.HOME_ICON])
    def test_home_page_icons(self, browser_final, main_page_fixture_final, icon_locator):
        page = main_page_fixture_final
        page.open_main_page_link(icon_locator)
        assert browser_final.current_url == f"{SiteData.url}welcome/", 'URL не соответствует домашней странице'
