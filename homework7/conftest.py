import pytest
from homework7.client import MysqlORMClient


def pytest_configure(config):
    mysql_orm_client = MysqlORMClient(user='root', password='Root123', db_name='devdivision')
    if not hasattr(config, "workerinput"):
        mysql_orm_client.recreate_db()

    mysql_orm_client.connect(db_created=True)

    config.mysql_orm_client = mysql_orm_client


@pytest.fixture(scope='session')
def mysql_orm_client(request) -> MysqlORMClient:
    client = request.config.mysql_orm_client
    yield client
    client.connection.close()


@pytest.fixture(scope='function')
def open_logfile():
    logfile = open("access.log", 'r')
    yield logfile
    logfile.close()
