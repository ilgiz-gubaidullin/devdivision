import pytest
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
        self.api_client_final.add_user(user_middle_name)
        assert self.find_in_db_by_username(user_middle_name['username']), 'Созданный пользователь не найден в БД'

    def test_add_user_status(self):
        username = random_str(15)
        user = self.data_manager.user(username=username)
        response = self.api_client_final.add_user(user)
        assert response.status_code == 201, 'Статус код должен быть 201'
        assert self.find_in_db_by_username(username), 'Созданный пользователь не найден в БД'

    @pytest.mark.parametrize('data_w_email', [
        DataManager.user(email=''),
        DataManager.user(email='123'),
        DataManager.user(email='123@'),
        DataManager.user(email='123@123'),
        DataManager.user(email='1.13'),
        DataManager.user(email='123@123..io'),
        DataManager.user(email='123@123.#'),
        DataManager.user(email='@123')])
    def test_user_invalid_email(self, data_w_email):
        response = self.api_client_final.add_user(data_w_email)
        assert response.status_code == 400
        assert not self.find_in_db_by_username(data_w_email['username']), 'Созданный пользователь найден в БД'

    @pytest.mark.parametrize('empty_field', [
        DataManager.user(name=''),
        DataManager.user(surname=''),
        DataManager.user(username=''),
        DataManager.user(password='')])
    def test_add_user_w_empty_field(self, empty_field):
        response = self.api_client_final.add_user(empty_field)
        assert response.status_code == 400
        assert not self.find_in_db_by_username(empty_field['username']), 'Созданный пользователь найден в БД'

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
        assert not self.find_in_db_by_username(exceeded_field['username']), 'Созданный пользователь найден в БД'


    @pytest.mark.parametrize('one_symbol_field', [
        DataManager.user(name=random_str(1)),
        DataManager.user(surname=random_str(1)),
        DataManager.user(middle_name=random_str(1)),
        DataManager.user(username=random_str(1)),
        DataManager.user(email=f"1@1.{random_str(1)}"),
        DataManager.user(password=random_str(1))])
    def test_add_user_w_one_symbol(self, one_symbol_field):
        response = self.api_client_final.add_user(one_symbol_field)
        assert self.find_in_db_by_username(one_symbol_field['username']), 'Созданный пользователь не найден в БД'

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

    def test_delete_user(self):
        username = random_str(15)
        user = self.data_manager.user(username=username)
        self.api_client_final.add_user(user)
        self.api_client_final.delete_user(username)
        assert not self.find_in_db_by_username(username), 'Созданный пользователь найден в БД'

    def test_change_user_password(self):
        user = self.data_manager.user()
        print(user['password'])
        self.api_client_final.add_user(user)
        self.api_client_final.change_user_password(user['username'], 'new_password')
        print(self.find_in_db_by_username(user['username'])[0].password)
        # assert self.find_in_db_by_username(user['username'])[0].password != user['password']

    def test_block_user(self):
        username = random_str(15)
        user = self.data_manager.user(username=username)
        self.api_client_final.add_user(user)
        self.api_client_final.block_user(username)
        assert self.find_in_db_by_username(username)[0].access == 0, "Значение access заблокированного пользователя не равно 0"

    def test_unblock_user(self):
        username = random_str(15)
        user = self.data_manager.user(username=username)
        self.api_client_final.add_user(user)
        self.api_client_final.block_user(username)
        assert self.find_in_db_by_username(username)[0].access == 0, "Значение access заблокированного пользователя не равно 0"
        self.api_client_final.unblock_user(username)
        assert self.find_in_db_by_username(username)[0].access == 1, "Значение access разблокированного пользователя не равно 1"
