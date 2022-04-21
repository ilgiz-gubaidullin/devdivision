import os
import shutil
import sys
import allure
import pytest
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from homework4.pages.login_page import LoginPage
from homework4.pages.main_page import MainPage
from selenium.webdriver import Chrome, ChromeOptions, Remote
from homework4.helpers.credentials import UserData
from datetime import datetime
from uuid import uuid4


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


def pytest_addoption(parser):
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')


@pytest.fixture(scope='session')
def ui_config(request):
    if request.config.getoption('--selenoid'):
        selenoid = 'http://127.0.0.1:4444'
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False

    else:
        selenoid = None
        vnc = False

    return {'selenoid': selenoid, 'vnc': vnc}


@pytest.fixture(scope='function')
def browser(request, test_dir, ui_config):
    """
    Открываем браузер и заходим на target.my.com
    """

    selenoid = ui_config['selenoid']
    vnc = ui_config['vnc']

    if selenoid is not None:
        capabilities = {
            'browserName': 'chrome',
            'version': '89.0',
            "pageLoadStrategy": "eager"
        }
        if vnc:
            capabilities['version'] += '_vnc'
            capabilities['enableVNC'] = True

        with allure.step("Открываем браузер"):
            driver = Remote(
                "http://127.0.0.1:4444/wd/hub",
                options=ChromeOptions(),
                desired_capabilities=capabilities)
    else:
        manager = ChromeDriverManager(log_level=0)
        path = manager.install()

        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"

        driver = Chrome(desired_capabilities=caps, executable_path=path)

    with allure.step("Заходим на target.my.com"):
        driver.maximize_window()
        driver.get('https://target.my.com/')

    with allure.step("Увеличиваем окно"):
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
def main_page_fixture(browser):
    """
    Логинимся и открываем главную страницу
    """
    page = LoginPage(browser)
    page.login(UserData.EMAIL, UserData.PASSWORD)

    return MainPage(browser)


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_dir = base_dir


@pytest.fixture()
def test_dir(request):
    # test_name = os.environ['PYTEST_CURRENT_TEST']
    test_name = request._pyfuncitem.nodeid
    test_dir = os.path.join(request.config.base_dir, test_name.replace('/', '_')
                            .replace(':', '_')
                            .replace('-', '_')
                            .replace('[', '_')
                            .replace(']', ''))
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture()
def unique_value():
    time_title = datetime.now().strftime('%H.%M.%S-%d.%m.%Y')
    randon_uuid_str = str(uuid4().hex)[0:6]
    return time_title + ':' + randon_uuid_str

