import pytest
from final_project.mysql_db.db_client import MysqlORMClient
from final_project.mysql_db.model import Test_users


class MysqlBase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client):
        self.mysql: MysqlORMClient = mysql_orm_client

    def find_in_db_by_username(self, value):
        self.mysql.session.commit()
        test_users = self.mysql.session.query(Test_users).filter_by(username=value).all()
        return test_users