import pytest
from homework7.client import MysqlORMClient


class MysqlBase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client, open_logfile):
        self.mysql: MysqlORMClient = mysql_orm_client
        self.logfile = open_logfile
