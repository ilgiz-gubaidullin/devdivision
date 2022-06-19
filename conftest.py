import shutil
import sys
from datetime import datetime
from uuid import uuid4
import logging
from homework4.fixtures import *
from homework5.fixtures import *


@pytest.fixture()
def upload_file_path(repo_root):
    return os.path.join(repo_root, "image_to_upload.jpg")


@pytest.fixture()
def logger(test_dir):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
    log_file = os.path.join(test_dir, 'debug.log')
    log_level = logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False

    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    allure.attach.file(log_file, 'debug.log', attachment_type=allure.attachment_type.TEXT)


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
                            .replace('>', '_')
                            .replace(' ', '_')
                            .replace(']', ''))
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture()
def unique_value():
    time_title = datetime.now().strftime('%H.%M.%S-%d.%m.%Y')
    randon_uuid_str = str(uuid4().hex)[0:6]
    return time_title + ':' + randon_uuid_str

