import pytest

from final_project.API.base import BaseAPITest
from faker import Faker


fake = Faker()


class TestApi(BaseAPITest):

    def test_app_status(self):
        response = self.api_client_final.get_app_status()
        assert response['status'] == 'ok'

    def test_add_user(self):
        user = self.data_manager.user(middle_name='')
        self.api_client_final.add_user(user)

    # @pytest.mark.parametrize(miss_field, )
    # def test_add_user_w_miss_field(self):

