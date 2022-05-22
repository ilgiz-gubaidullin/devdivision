import pytest
from homework5.client import ApiClient
from homework4.helpers.credentials import UserData
from faker import Faker


fake = Faker()


@pytest.fixture()
def fake_email():
    return fake.url()


@pytest.fixture(scope='session')
def cookies(api_client):
    return api_client.session.cookies


@pytest.fixture(scope='session')
def api_client():
    client = ApiClient("https://target.my.com/")
    client.post_user_auth(UserData.EMAIL, UserData.PASSWORD)

    return client
