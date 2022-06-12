import pytest
from final_project.helpers.datamanager import DataManager
from final_project.API.base import BaseAPITest
from faker import Faker
from final_project.helpers.utility_functions import random_str


fake = Faker()


class TestApi(BaseAPITest):

    def test_app_status(self):
        response = self.api_client_final.get_app_status()
        assert response['status'] == 'ok'


    @pytest.mark.parametrize('user_middle_name', [
        DataManager.user(middle_name=''),
        DataManager.user(middle_name='Hose')])
    def test_add_user(self, user_middle_name):
        response = self.api_client_final.add_user(user_middle_name)


    def test_add_user_status(self):
        user = self.data_manager.user()
        response = self.api_client_final.add_user(user)
        assert response.status_code == 201


    @pytest.mark.parametrize('data_w_email', [
        DataManager.user(email=''),
        DataManager.user(email='123'),
        DataManager.user(email='123@'),
        DataManager.user(email='123@123'),
        DataManager.user(email='@123')])
    def test_user_email_field(self, data_w_email):
        response = self.api_client_final.add_user(data_w_email)
        assert response.status_code == 400


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
    def test_add_user_w_empty_field(self, exceeded_field):
        response = self.api_client_final.add_user(exceeded_field)
        assert response.status_code == 400


