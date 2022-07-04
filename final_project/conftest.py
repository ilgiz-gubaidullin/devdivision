from final_project.helpers.site_data import SiteData
from final_project.API.api_client import ApiClientFinal
from final_project.mysql_db.db_client import MysqlORMClient
from final_project.UI.pages.main_page import MainPage
from final_project.helpers.datamanager import DataManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import Chrome, ChromeOptions, Remote
import allure
import pytest
import os


@pytest.fixture(scope='session')
def api_client_final():
    client = ApiClientFinal(SiteData.url)
    client.post_user_auth(SiteData.main_user, SiteData.main_user_pass)
    return client


@pytest.fixture(scope='function')
def add_user_return_request(api_client_final):
    """
    Создание пользователя и возвращение запроса
    """
    user = DataManager.user()
    response = api_client_final.add_user(user)
    return user, response


def pytest_configure(config):
    mysql_orm_client = MysqlORMClient(user='test_qa', password='qa_test', db_name='vkeducation')
    mysql_orm_client.connect()
    config.mysql_orm_client = mysql_orm_client


@pytest.fixture(scope='session')
def mysql_orm_client(request) -> MysqlORMClient:
    client = request.config.mysql_orm_client
    yield client
    client.connection.close()


@pytest.fixture(scope='session')
def cookies_final(api_client_final):
    return api_client_final.session.cookies


@pytest.fixture(scope='session')
def ui_config_final(request):
    if request.config.getoption('--selenoid'):
        selenoid = 'http://selenoid_container:4444/'
        vnc = False

    else:
        selenoid = None
        vnc = False

    return {'selenoid': selenoid, 'vnc': vnc}


@pytest.fixture(scope='function')
def browser_final(request, test_dir, ui_config_final, cookies_final):

    selenoid = ui_config_final['selenoid']

    if selenoid is not None:
        capabilities = {
            'browserName': 'chrome',
            'version': '89.0',
            'applicationContainers': ['my-cool-app']
        }

        with allure.step("Открываем браузер"):
            driver = Remote(
                "http://selenoid_container:4444/wd/hub",
                options=ChromeOptions(),
                desired_capabilities=capabilities)
    else:
        manager = ChromeDriverManager(log_level=0)
        path = manager.install()

        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"

        driver = Chrome(desired_capabilities=caps, executable_path=path)

    driver.get(SiteData.url)
    driver.maximize_window()

    yield driver

    if request.node.rep_setup.failed or (getattr(request.node, "rep_call") and request.node.rep_call.failed):
        screenshot_path = os.path.join(test_dir, 'failure.png')
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, 'failure.png', attachment_type=allure.attachment_type.PNG)

        browser_log_path = os.path.join(test_dir, 'browser.log')
        with open(browser_log_path, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_log_path, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)

    # Закрыть браузер
    with allure.step("Закрываем браузер"):
        driver.quit()


@pytest.fixture
def main_page_fixture_final(browser_final, request, api_client_final):
    """
    Логинимся через куки и открываем главную страницу
    """
    cookies = request.getfixturevalue('cookies_final')
    for cookie in cookies:
        cookie_dict = {
            'name': cookie.name,
            'value': cookie.value,
        }
        browser_final.add_cookie(cookie_dict)

    browser_final.refresh()
    return MainPage(browser_final)


@pytest.fixture(scope='function')
def open_create_account_page(browser_final):
    """
    Открываем страницу регистрации пользователя
    """
    browser_final.get(f"{SiteData.url}reg")

