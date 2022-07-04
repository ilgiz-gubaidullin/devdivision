import pytest
from final_project.UI.ui_base import BaseUISuiteTest
import allure
from final_project.UI.pages.login_page import LoginPage
from final_project.UI.pages.reg_page import RegPage
from final_project.helpers.site_data import SiteData, MainPageLinks
from final_project.helpers.locators import MainPageLocators
from selenium.webdriver import ActionChains
from final_project.helpers.datamanager import DataManager
from final_project.mysql_db.db_base import MysqlBase
from final_project.helpers.utility_functions import random_str


TEST_CASES_LINK = SiteData.test_cases


@allure.testcase(TEST_CASES_LINK, 'Test cases link')
class TestMainPageUI(BaseUISuiteTest, MysqlBase):

    @pytest.mark.UI_FINAL
    @pytest.mark.parametrize('username, password', (('wrong_username', 'wrong_pass'),
                                                    (SiteData.main_user, 'wrong_pass'),
                                                    ('wrong_username', SiteData.main_user_pass),
                                                    ('', '')))
    def test_negative_login(self, browser_final, username, password):
        """
        Негативный тест на логин, проверка на изменение url
        """
        with allure.step("Процесс логина"):
            page = LoginPage(browser_final)
            page.login(username, password)
        with allure.step("Проверка логина пользователя"):
            assert browser_final.current_url != f"{SiteData.url}welcome", 'URL не должен меняться на успешный'

    @pytest.mark.UI_FINAL
    @pytest.mark.parametrize('username, password', ((SiteData.main_user, SiteData.main_user_pass),
                                                    (f"   {SiteData.main_user}   ", f"  {SiteData.main_user_pass}  ")))
    def test_login_success(self, browser_final, username, password):
        """
        Позитивный тест на логин, также же на обработку пробелов перед кредами, проверка на изменение url
        """
        with allure.step("Процесс логина"):
            page = LoginPage(browser_final)
            page.login(username, password)
        with allure.step("Проверка логина пользователя"):
            assert browser_final.current_url == f"{SiteData.url}welcome/", 'URL должен меняться на успешный'
            page.check_user_logged(username)

    @pytest.mark.UI_FINAL
    @pytest.mark.parametrize('link_locator', [MainPageLocators.WHAT_IS_API_ICON,
                                              MainPageLocators.INTERNET_FUTURE_ICON,
                                              MainPageLocators.SMTP_ICON])
    def test_links_main_page_container(self, browser_final, main_page_fixture_final, link_locator):
        """
        Проверка на то что можно пройти по ссылкам иконок на главной странице, и что это ссылки находятся в списке предоставленных
        """
        page = main_page_fixture_final
        page.open_main_page_link(link_locator)
        browser_final.switch_to.window(browser_final.window_handles[1])
        assert browser_final.current_url in MainPageLinks.container_links

    @pytest.mark.UI_FINAL
    @pytest.mark.parametrize('hover_element, link_locator', ((MainPageLocators.PYTHON_HOVER, MainPageLocators.PYTHON_HISTORY),
                                                             (MainPageLocators.PYTHON_HOVER, MainPageLocators.ABOUT_FLASK),
                                                             (MainPageLocators.LINUX_HOVER, MainPageLocators.DOWNLOAD_CENTOS),
                                                             (MainPageLocators.NETWORK_HOVER, MainPageLocators.WIRESHARK_NEWS),
                                                             (MainPageLocators.NETWORK_HOVER, MainPageLocators.WIRESHARK_DOWNLOAD),
                                                             (MainPageLocators.NETWORK_HOVER, MainPageLocators.TCDUMP_EXAMPLES),
                                                             ))
    def test_links_main_page_header(self, browser_final, main_page_fixture_final, hover_element, link_locator):
        """
        Проверка на то что можно пройти по ссылкам иконок в хэдере, и что это ссылки находятся в списке предоставленных
        """
        page = main_page_fixture_final
        element = page.move_cursor(hover_element)
        ActionChains(browser_final).move_to_element(element).perform()
        page.open_main_page_link(link_locator)
        browser_final.switch_to.window(browser_final.window_handles[1])
        assert browser_final.current_url in MainPageLinks.header_links

    @pytest.mark.UI_FINAL
    def test_footer_str_present(self, browser_final, main_page_fixture_final):
        """
        Проверка на то что в футере присутствует строка с фразой
        """
        page = main_page_fixture_final
        page.check_footer_str_present()

    @pytest.mark.UI_FINAL
    def test_logout(self, browser_final, main_page_fixture_final):
        """
        Позитивный тест на логаут
        """
        page = main_page_fixture_final
        page.make_logout()
        assert browser_final.current_url == f"{SiteData.url}login", 'URL не соответствует странице логина'

    @pytest.mark.UI_FINAL
    @pytest.mark.parametrize('icon_locator', [MainPageLocators.TM_ICON,
                                              MainPageLocators.HOME_ICON])
    def test_home_page_icons(self, browser_final, main_page_fixture_final, icon_locator):
        """
        Проверка на то что можно пройти по ссылкам иконок на панели, которые ведут на домашнюю страницу
        """
        page = main_page_fixture_final
        page.open_main_page_link(icon_locator)
        assert browser_final.current_url == f"{SiteData.url}welcome/", 'URL не соответствует домашней странице'

    @pytest.mark.UI_FINAL
    def test_reg_form_open(self, browser_final):
        """
        Тест на открытие страницы регистрации
        """
        page = LoginPage(browser_final)
        page.open_reg_form()
        assert browser_final.current_url == f"{SiteData.url}reg", 'URL не соответствует странице регистрации'

    @pytest.mark.UI_FINAL
    @pytest.mark.parametrize('user_middle_name', [
        DataManager.user(middle_name=''),
        DataManager.user(middle_name='Hose')])
    def test_create_account(self, browser_final, user_middle_name, open_create_account_page):
        """
        Проверка на регистрацию пользователя, с и без middle_name
        """
        page = RegPage(browser_final)
        page.create_account(user_middle_name)
        assert browser_final.current_url == f"{SiteData.url}welcome/", 'URL не соответствует домашней странице'
        assert self.find_in_db_by_username(user_middle_name['username']), 'Созданный пользователь не найден в БД'
        assert self.find_in_db_by_username(user_middle_name['username'])[0].access == 1, "Значение access пользователя не равно 1"

    @pytest.mark.UI_FINAL
    def test_create_acc_without_checkbox(self, browser_final, open_create_account_page):
        """
        Проверка на регистрацию пользователя, без клика чекбокса
        """
        page = RegPage(browser_final)
        user = DataManager.user()
        page.create_account(user, checkbox=False)
        assert browser_final.current_url != f"{SiteData.url}welcome/", 'URL соответствует домашней странице'
        assert not self.find_in_db_by_username(user['username']), 'Созданный пользователь найден в БД'

    @pytest.mark.UI_FINAL
    @pytest.mark.parametrize('user_data_w_email', [
        DataManager.user(email=''),
        DataManager.user(email='123'),
        DataManager.user(email='123@'),
        DataManager.user(email='123@123'),
        DataManager.user(email='1.13'),
        DataManager.user(email='123@123..io'),
        DataManager.user(email='123@123.#'),
        DataManager.user(email='@123')])
    def test_create_acc_w_invalid_email(self, user_data_w_email, browser_final, open_create_account_page):
        """
        Проверка на регистрацию пользователя, с невалидным email
        """
        page = RegPage(browser_final)
        page.create_account(user_data_w_email)
        assert browser_final.current_url != f"{SiteData.url}welcome/", 'URL соответствует домашней странице'
        assert not self.find_in_db_by_username(user_data_w_email['username']), 'Созданный пользователь найден в БД'

    @pytest.mark.UI_FINAL
    @pytest.mark.parametrize('user_data_w_empty_field', [
        DataManager.user(name=''),
        DataManager.user(surname=''),
        DataManager.user(username=''),
        DataManager.user(password='')])
    def test_create_acc_w_empty_field(self, user_data_w_empty_field, browser_final, open_create_account_page):
        """
        Проверка на регистрацию пользователя, с пустым обязательным полем
        """
        page = RegPage(browser_final)
        page.create_account(user_data_w_empty_field)
        assert browser_final.current_url != f"{SiteData.url}welcome/", 'URL соответствует домашней странице'
        assert not self.find_in_db_by_username(user_data_w_empty_field['username']), 'Созданный пользователь найден в БД'

    @pytest.mark.UI_FINAL
    @pytest.mark.parametrize('user_data_w_exceeded_field', [
        DataManager.user(name=random_str(256)),
        DataManager.user(surname=random_str(256)),
        DataManager.user(middle_name=random_str(256)),
        DataManager.user(username=random_str(17)),
        DataManager.user(email=f"123@{random_str(65)}"),
        DataManager.user(password=random_str(256))])
    def test_create_acc_w_exceeded_field(self, user_data_w_exceeded_field, browser_final, open_create_account_page):
        """
        Проверка на регистрацию пользователя, с полем превышающим максимальную длину, указанную в БД
        """
        page = RegPage(browser_final)
        page.create_account(user_data_w_exceeded_field)
        assert browser_final.current_url != f"{SiteData.url}welcome/", 'URL соответствует домашней странице'
        assert not self.find_in_db_by_username(user_data_w_exceeded_field['username']), 'Созданный пользователь найден в БД'

    @pytest.mark.UI_FINAL
    @pytest.mark.parametrize('user_data_w_min_symbol_field', [
        DataManager.user(name=random_str(1)),
        DataManager.user(surname=random_str(1)),
        DataManager.user(middle_name=random_str(1)),
        DataManager.user(username=random_str(6)),
        DataManager.user(email=f"{random_str(1)}@{random_str(1)}.qw"),
        DataManager.user(password=random_str(1))])
    def test_create_acc_w_min_symbol_field(self, user_data_w_min_symbol_field, browser_final, open_create_account_page):
        """
        Позитивная проверка на регистрацию пользователя, с минимальными значениями в поле
        """
        page = RegPage(browser_final)
        page.create_account(user_data_w_min_symbol_field)
        assert browser_final.current_url == f"{SiteData.url}welcome/", 'URL не соответствует домашней странице'
        assert self.find_in_db_by_username(user_data_w_min_symbol_field['username']), 'Созданный пользователь не найден в БД'

    @pytest.mark.UI_FINAL
    @pytest.mark.parametrize('user_data_w_space_in_field', [
        DataManager.user(name=f"   {random_str(10)}"),
        DataManager.user(surname=f"   {random_str(10)}"),
        DataManager.user(middle_name=f"   {random_str(10)}"),
        DataManager.user(username=f"   {random_str(10)}"),
        DataManager.user(email=f"  {random_str(10)}@1.qw"),
        DataManager.user(password=f"   {random_str(10)}")])
    def test_create_acc_w_space_in_field(self, user_data_w_space_in_field, browser_final, open_create_account_page):
        """
        Проверка на регистрацию пользователя, с пробелами в полях
        """
        page = RegPage(browser_final)
        page.create_account(user_data_w_space_in_field)
        assert browser_final.current_url == f"{SiteData.url}welcome/", 'URL не соответствует домашней странице'
        assert self.find_in_db_by_username(user_data_w_space_in_field['username']), 'Созданный пользователь не найден в БД'

    @pytest.mark.UI_FINAL
    @pytest.mark.parametrize('user_data', [
        DataManager.user(username='main_user'),
        DataManager.user(email='qwe@qwe.qwe')])
    def test_create_acc_username_email_uniqueness(self, user_data, browser_final, open_create_account_page):
        """
        Проверка на регистрацию пользователя, с неуникальными значениями email, username
        """
        page = RegPage(browser_final)
        page.create_account(user_data)
        assert browser_final.current_url != f"{SiteData.url}welcome/", 'URL соответствует домашней странице'
