import pytest
from final_project.helpers.site_data import SiteData
from final_project.API.api_client import ApiClientFinal
from final_project.mysql_db.db_client import MysqlORMClient


@pytest.fixture(scope='session')
def api_client_final():
    client = ApiClientFinal(SiteData.url)
    client.post_user_auth(SiteData.main_user, SiteData.main_user_pass)
    return client


def pytest_configure(config):
    mysql_orm_client = MysqlORMClient(user='test_qa', password='qa_test', db_name='vkeducation')
    mysql_orm_client.connect()
    config.mysql_orm_client = mysql_orm_client


@pytest.fixture(scope='session')
def mysql_orm_client(request) -> MysqlORMClient:
    client = request.config.mysql_orm_client
    yield client
    client.connection.close()
