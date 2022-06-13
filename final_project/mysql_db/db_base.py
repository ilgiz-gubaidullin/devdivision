import pytest
from final_project.mysql_db.db_client import MysqlORMClient


class MysqlBase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client):
        self.mysql: MysqlORMClient = mysql_orm_client
