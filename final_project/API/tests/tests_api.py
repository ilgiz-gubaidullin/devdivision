import pytest
import sqlalchemy

from final_project.helpers.datamanager import DataManager
from final_project.API.api_base import BaseAPITest
from faker import Faker
from final_project.helpers.utility_functions import random_str
from final_project.helpers.site_data import SiteData
from final_project.mysql_db.db_base import MysqlBase


fake = Faker()


class TestApi(BaseAPITest, MysqlBase):

    def test_app_status(self):
        response = self.api_client_final.get_app_status()
        assert response['status'] == 'ok'


    @pytest.mark.parametrize('user_middle_name', [
        DataManager.user(middle_name=''),
        DataManager.user(middle_name='Hose')])
    def test_add_user(self, user_middle_name):
        response = self.api_client_final.add_user(user_middle_name)


    def test_add_user_status(self):
        # user = self.data_manager.user()
        # response = self.api_client_final.add_user(user)
        # assert response.status_code == 201

        table = self.mysql.test_users_table
        # self.mysql.execute_query(self.mysql.test_users_table.where)
        # query = table.select()
        print(table.columns.keys())


    @pytest.mark.parametrize('data_w_email', [
        DataManager.user(email=''),
        DataManager.user(email='123'),
        DataManager.user(email='123@'),
        DataManager.user(email='123@123'),
        DataManager.user(email='1.13'),
        DataManager.user(email='123@123.1'),
        DataManager.user(email='123@123..io'),
        DataManager.user(email='123@123.#'),
        DataManager.user(email='@123')])
    def test_user_invalid_email(self, data_w_email):
        response = self.api_client_final.add_user(data_w_email)
        print(response.text)
        print(response.status_code)
        # assert response.status_code == 400


    @pytest.mark.parametrize('empty_field', [
        DataManager.user(name=''),
        DataManager.user(surname=''),
        DataManager.user(username=''),
        DataManager.user(password='')])
    def test_add_user_w_empty_field(self, empty_field):
        response = self.api_client_final.add_user(empty_field)
        assert response.status_code == 400


    @pytest.mark.parametrize('exceeded_field', [
        DataManager.user(name=random_str(256)),
        DataManager.user(surname=random_str(256)),
        DataManager.user(middle_name=random_str(256)),
        DataManager.user(username=random_str(17)),
        DataManager.user(email=f"123@{random_str(65)}"),
        DataManager.user(password=random_str(256))])
    def test_add_user_w_exceeded_field(self, exceeded_field):
        response = self.api_client_final.add_user(exceeded_field)
        assert response.status_code == 400

    @pytest.mark.parametrize('one_symbol_field', [
        DataManager.user(name=random_str(1)),
        DataManager.user(surname=random_str(1)),
        DataManager.user(middle_name=random_str(1)),
        DataManager.user(username=random_str(1)),
        DataManager.user(email=f"1@1.{random_str(1)}"),
        DataManager.user(password=random_str(1))])
    def test_add_user_w_one_symbol(self, one_symbol_field):
        response = self.api_client_final.add_user(one_symbol_field)
        print(response.text)
        print(response.status_code)


    @pytest.mark.parametrize('username, password', (('wrong_username', 'wrong_pass'),
                                                 (SiteData.main_user, 'wrong_pass'),
                                                 ('wrong_username', SiteData.main_user_pass),
                                                 ('', '')))
    def test_negative_login(self, username, password):
        self.api_client_final.session.cookies.clear_session_cookies()
        self.api_client_final.post_user_auth(username=username, password=password)
        response = self.api_client_final.add_user(self.data_manager.user())
        assert response.status_code == 401

    def test_logout(self):
        self.api_client_final.logout()
        response = self.api_client_final.add_user(self.data_manager.user())
        assert response.status_code == 401
