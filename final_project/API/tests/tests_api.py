import pytest
from final_project.helpers.datamanager import DataManager
from final_project.API.api_base import BaseAPITest
from faker import Faker
from final_project.helpers.utility_functions import random_str
from final_project.helpers.site_data import SiteData
from final_project.mysql_db.db_base import MysqlBase
from final_project.API.api_client import ApiClientFinal
import allure


fake = Faker()
TEST_CASES_LINK = SiteData.test_cases


@allure.testcase(TEST_CASES_LINK, 'Test cases link')
class TestApi(BaseAPITest, MysqlBase):

    @pytest.mark.API_FINAL
    def test_app_status(self):
        """
        Получение статуса активного приложения
        """
        response = self.api_client_final.get_app_status()
        assert response['status'] == 'ok'

    @pytest.mark.API_FINAL
    @pytest.mark.parametrize('user_middle_name', [
        DataManager.user(middle_name=''),
        DataManager.user(middle_name='Hose')])
    def test_add_user(self, user_middle_name):
        """
        Добавление пользователя с и без middle_name
        """
        self.api_client_final.add_user(user_middle_name)
        assert self.find_in_db_by_username(user_middle_name['username']), 'Созданный пользователь не найден в БД'

    @pytest.mark.API_FINAL
    def test_add_user_request_status(self, add_user_return_request):
        """
        Проверка статуса запроса добавления пользователя
        """
        user, response = add_user_return_request
        assert self.find_in_db_by_username(user['username']), 'Созданный пользователь не найден в БД'
        assert self.find_in_db_by_username(user['username'])[0].access == 1, "Значение access пользователя не равно 1"
        assert response.status_code == 201, 'Статус код должен быть 201'

    @pytest.mark.API_FINAL
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
        """
        Добавление пользователя с невалидным email
        """
        response = self.api_client_final.add_user(data_w_email)
        assert response.status_code == 400, f'Сервер должен возвращать 400 ошибку, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    @pytest.mark.parametrize('empty_field', [
        DataManager.user(name=''),
        DataManager.user(surname=''),
        DataManager.user(username=''),
        DataManager.user(password='')])
    def test_add_user_w_empty_field(self, empty_field):
        """
        Добавление пользователя без обязательного поля
        """
        response = self.api_client_final.add_user(empty_field)
        assert response.status_code == 400, f'Сервер должен возвращать 400 ошибку, но сейчас вернул {response.status_code}'
        assert not self.find_in_db_by_username(empty_field['username']), 'Созданный пользователь найден в БД, но этот пользователь не должен существовать'

    @pytest.mark.API_FINAL
    @pytest.mark.parametrize('exceeded_field', [
        DataManager.user(name=random_str(256)),
        DataManager.user(surname=random_str(256)),
        DataManager.user(middle_name=random_str(256)),
        DataManager.user(username=random_str(17)),
        DataManager.user(email=f"123@{random_str(65)}"),
        DataManager.user(password=random_str(256))])
    def test_add_user_w_exceeded_field(self, exceeded_field):
        """
        Добавление пользователя с длиной поля, превышающим значение в БД
        """
        response = self.api_client_final.add_user(exceeded_field)
        assert response.status_code == 400, f'Сервер должен возвращать 400 ошибку, но сейчас вернул {response.status_code}'
        assert not self.find_in_db_by_username(exceeded_field['username']), 'Созданный пользователь найден в БД'

    @pytest.mark.API_FINAL
    @pytest.mark.parametrize('one_symbol_field', [
        DataManager.user(name=random_str(1)),
        DataManager.user(surname=random_str(1)),
        DataManager.user(middle_name=random_str(1)),
        DataManager.user(username=random_str(1)),
        DataManager.user(email=f"1@1.{random_str(1)}"),
        DataManager.user(password=random_str(1))])
    def test_add_user_w_one_symbol(self, one_symbol_field):
        """
        Добавление пользователя с одним символом в поле
        """
        self.api_client_final.add_user(one_symbol_field)
        assert self.find_in_db_by_username(one_symbol_field['username']), 'Созданный пользователь не найден в БД'

    @pytest.mark.API_FINAL
    @pytest.mark.parametrize('username, password', (('wrong_username', 'wrong_pass'),
                                                 (SiteData.main_user, 'wrong_pass'),
                                                 ('wrong_username', SiteData.main_user_pass),
                                                 ('', '')))
    def test_negative_login(self, username, password):
        """
        Логин с невалидными значениями
        """
        login_test_client = ApiClientFinal(SiteData.url)
        login_test_client.post_user_auth(username=username, password=password)
        response = login_test_client.add_user(self.data_manager.user())
        assert response.status_code == 401, f'Сервер должен возвращать 401 ошибку, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_logout(self):
        """
        Логаут и попытка использовать метод добавления пользователя
        """
        login_test_client = ApiClientFinal(SiteData.url)
        login_test_client.post_user_auth(username=SiteData.main_user, password=SiteData.main_user_pass)
        login_test_client.logout()
        response = login_test_client.add_user(self.data_manager.user())
        assert response.status_code == 401, f'Сервер должен возвращать 401 ошибку, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_auth_to_use_methods(self, add_user_return_request):
        """
        Логаут и попытка использовать методы требующие авторизации
        """
        login_test_client = ApiClientFinal(SiteData.url)
        login_test_client.post_user_auth(username=SiteData.main_user, password=SiteData.main_user_pass)
        login_test_client.logout()

        user, response = add_user_return_request

        response = login_test_client.delete_user(user['username'])
        assert response.status_code == 401, f'Сервер должен возвращать 401 ошибку, но сейчас вернул {response.status_code}'

        response = login_test_client.change_user_password(user['username'], 'new_password')
        assert response.status_code == 401, f'Сервер должен возвращать 401 ошибку, но сейчас вернул {response.status_code}'

        response = login_test_client.block_user(user['username'])
        assert response.status_code == 401, f'Сервер должен возвращать 401 ошибку, но сейчас вернул {response.status_code}'

        response = login_test_client.unblock_user(user['username'])
        assert response.status_code == 401, f'Сервер должен возвращать 401 ошибку, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_delete_user(self, add_user_return_request):
        """
        Удаление пользователя и проверка на его отсутствие в БД и статус кода
        """
        user = add_user_return_request[0]
        response = self.api_client_final.delete_user(user['username'])
        assert not self.find_in_db_by_username(user['username']), 'Созданный пользователь найден в БД'
        assert response.status_code == 204, f'Сервер должен возвращать 204, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_change_user_password(self, add_user_return_request):
        """
        Изменение пароля пользователя, проверка на измение в БД, и статус кода
        """
        user = add_user_return_request[0]
        response = self.api_client_final.change_user_password(user['username'], 'new_password')
        assert self.find_in_db_by_username(user['username'])[0].password != user['password']
        assert response.status_code == 200, f'Сервер должен возвращать 200, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_change_user_password_to_existing(self):
        """
        Попытка изменить пароль пользователя на существующий, проверка статус кода
        """
        user = self.data_manager.user(password='existing_password')
        self.api_client_final.add_user(user)
        response = self.api_client_final.change_user_password(user['username'], 'existing_password')
        assert response.status_code == 400, f'Сервер должен возвращать 400 ошибку, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_block_user(self, add_user_return_request):
        """
        Блокирование пользователя:
        - сначала создание пользователя, проверка что значение active=1, наличие непустого значения start_active_time
        - блокировка пользователя, проверка статус кода, поле access=0 в БД
        - попытка залогиниться
        """
        user = add_user_return_request[0]

        login_test_client = ApiClientFinal(SiteData.url)
        login_test_client.post_user_auth(username=user['username'], password=user['password'])
        assert self.find_in_db_by_username(user['username'])[0].active == 1, "Значение active залогиненного пользователя не равно 1"
        assert self.find_in_db_by_username(user['username'])[0].start_active_time is not None, "Значение start_active_time залогиненного пользователя пустое"

        response = self.api_client_final.block_user(user['username'])
        assert response.status_code == 200, f'Сервер должен возвращать 200 ошибку, но сейчас вернул {response.status_code}'
        assert self.find_in_db_by_username(user['username'])[0].access == 0, "Значение access заблокированного пользователя не равно 0"

        response = login_test_client.add_user(self.data_manager.user())
        assert response.status_code == 401, f'Сервер должен возвращать 401 ошибку, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_unblock_user(self):
        """
        Разблокировка пользователя, проверка статус кода, поле access=0 в БД.
        В конце теста заново блокирую пользователя, для следующих тестов.

        """
        response = self.api_client_final.unblock_user('blocked_user1')
        assert response.status_code == 200, f'Сервер должен возвращать 200 ошибку, но сейчас вернул {response.status_code}'
        assert self.find_in_db_by_username('blocked_user1')[0].access == 1, "Значение access разблокированного пользователя не равно 1"

        self.api_client_final.block_user('blocked_user1')
        assert self.find_in_db_by_username('blocked_user1')[0].access == 0, "Значение access заблокированного пользователя не равно 0"

    @pytest.mark.API_FINAL
    def test_login_as_blocked_user(self):
        """
        Попытка залогиниться как заблокированный пользователь:
        """
        login_test_client = ApiClientFinal(SiteData.url)
        response = login_test_client.post_user_auth(username='blocked_user2', password='blocked_user2')
        assert response.status_code == 401, f'Сервер должен возвращать 401 ошибку, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_delete_non_existing_user(self):
        """
        Попытка удалить несуществующего пользователя
        """
        response = self.api_client_final.delete_user(random_str(15))
        assert response.status_code == 404, f'Сервер должен возвращать 404 ошибку, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_block_non_existing_user(self):
        """
        Попытка заблокировать несуществующего пользователя
        """
        response = self.api_client_final.block_user(random_str(15))
        assert response.status_code == 404, f'Сервер должен возвращать 404 ошибку, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_unblock_non_existing_user(self):
        """
        Попытка разблокировать несуществующего пользователя
        """
        response = self.api_client_final.unblock_user(random_str(15))
        assert response.status_code == 404, f'Сервер должен возвращать 404 ошибку, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_change_non_existing_user_password(self):
        """
        Попытка изменить пароль несуществующего пользователя
        """
        response = self.api_client_final.change_user_password(random_str(15), 'new_password')
        assert response.status_code == 404, f'Сервер должен возвращать 404 ошибку, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_user_email_uniqueness(self, add_user_return_request):
        """
        Проверка уникальности почты при создании пользователя
        """
        user = add_user_return_request[0]
        created_user_email = self.find_in_db_by_username(user['username'])[0].email
        user = self.data_manager.user(email=created_user_email)
        response = self.api_client_final.add_user(user)
        assert response.status_code == 400, f'Сервер должен возвращать 400 ошибку, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_username_uniqueness(self, add_user_return_request):
        """
        Проверка уникальности username при создании пользователя
        """
        user = add_user_return_request[0]
        created_username = self.find_in_db_by_username(user['username'])[0].username
        user = self.data_manager.user(username=created_username)
        response = self.api_client_final.add_user(user)
        assert response.status_code == 400, f'Сервер должен возвращать 400 ошибку, но сейчас вернул {response.status_code}'

    @pytest.mark.API_FINAL
    def test_spaces_trim_login(self):
        """
        Проверка логина с пробелами перед и после кред
        """
        login_test_client = ApiClientFinal(SiteData.url)
        response = login_test_client.post_user_auth(username=f" {SiteData.main_user} ", password=f" {SiteData.main_user_pass} ")
        assert response.status_code != 401, f'Сервер не должен возвращать 401 ошибку, но сейчас вернул'
        assert dict(response.cookies) is not None

    @pytest.mark.API_FINAL
    def test_positive_get_vk_id(self):
        """
        Проверка на получение vk_id пользователя, у которого есть vk_id
        """
        response = self.api_client_final.get_vk_id(SiteData.main_user)
        assert response.status_code == 200
        assert response.json()['vk_id'] == 1234567890
        assert response.headers['Content-Type'] == 'application/json'

    @pytest.mark.API_FINAL
    def test_negative_get_vk_id(self):
        """
        Проверка на получение vk_id пользователя, у которого нет vk_id
        """
        response = self.api_client_final.get_vk_id(random_str(10))
        assert response.status_code == 404
        assert response.json() == {}
        assert response.headers['Content-Type'] == 'application/json'

    @pytest.mark.API_FINAL
    @pytest.mark.parametrize('space_field', [
        DataManager.user(name=f"   {random_str(10)}"),
        DataManager.user(surname=f"   {random_str(10)}"),
        DataManager.user(middle_name=f"   {random_str(10)}"),
        DataManager.user(username=f"   {random_str(10)}"),
        DataManager.user(email=f"  1@1.{random_str(1)}"),
        DataManager.user(password=f"   {random_str(10)}")])
    def test_add_user_w_space_at_field(self, space_field):
        """
        Добавление пользователя у которого есть пробелы перед значениями в полях
        """
        response = self.api_client_final.add_user(space_field)
        assert response.status_code == 400, f'Сервер должен возвращать 400 ошибку, но сейчас вернул {response.status_code}'
