import allure
import requests
from urllib.parse import urljoin
from requests import HTTPError
from jsonschema import validate
import json
import logging
from json import JSONDecodeError
from faker import Faker


fake = Faker()
logger = logging.getLogger("test")


class RequestFailureException(HTTPError, AssertionError):
    pass


class AuthFailureException(HTTPError, AssertionError):
    pass


class ApiClientFinal:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    @staticmethod
    def _logging_pre(url, headers, data, expected_status):
        text = f'Performing request:\n' \
               f'URL: {url}\n' \
               f'HEADERS: {headers}\n' \
               f'DATA: {data}\n\n' \
               f'expected status: {expected_status}\n\n'

        allure.attach(text, 'request', attachment_type=allure.attachment_type.TEXT)
        logger.info(text)

    @staticmethod
    def _logging_post(response):
        try:
            data = json.dumps(response.json(), indent=4)
        except JSONDecodeError:
            data = response.text

        text = 'Got response:\n' \
               f'RESPONSE STATUS: {response.status_code}\n' \
               f'RESPONSE CONTENT: {data}\n\n'

        allure.attach(text, 'response', attachment_type=allure.attachment_type.TEXT)
        logger.info(text)

    def _request(self, method, location, headers=None, params=None, data=None, json_data=None,
                 check_schema=None, check_status=True, expect_status=200, jsonify=True, check_content_json=True):
        url = urljoin(self.base_url, location)
        logger.info('-' * 100 + '\n')

        self._logging_pre(url, headers, data or json_data, expect_status)

        response = self.session.request(method, url, headers=headers, params=params, data=data, json=json_data)

        self._logging_post(response)
        # if check_status=True, check status for 4xx and 5xx
        if check_status:
            response.raise_for_status()

        # check for expected status
        if expect_status and response.status_code != expect_status:
            raise RequestFailureException(f'Request {url} failed with [{response.status_code}]: {response.text}',
                                          response=response)

        # check schema
        if check_schema is not None:
            validate(instance=response.json(), schema=check_schema)

        if check_content_json:
            assert response.headers['Content-Type'] == 'application/json'

        if jsonify:
            return response.json()

        return response

    def post_user_auth(self, username, password):
        response = self.session.post(
            "http://127.0.0.1:8082/login",
            data={"username": username,"password": password},
            allow_redirects=False)
        return response

    def get_app_status(self):
        location = 'status'
        response = self._request("GET", location)
        return response

    def add_user(self, data):
        location = 'api/user'
        return self._request('POST', location, json_data=data, check_status=False, expect_status=0, jsonify=False)

    def logout(self):
        location = 'logout'
        return self._request('GET', location, check_content_json=False, jsonify=False)

    def delete_user(self, username):
        location = f'api/user/{username}'
        return self._request('DELETE', location, check_content_json=False, jsonify=False, check_status=False, expect_status=0)

    def change_user_password(self, username, password):
        location = f'api/user/{username}/change-password'
        data = {"password": password}
        return self._request('PUT', location, check_content_json=False, json_data=data, check_status=False, expect_status=0, jsonify=False)

    def block_user(self, username):
        location = f'api/user/{username}/block'
        return self._request('POST', location, check_content_json=False, check_status=False, expect_status=0, jsonify=False)

    def unblock_user(self, username):
        location = f"api/user/{username}/accept"
        return self._request('POST', location, check_content_json=False, check_status=False, expect_status=0, jsonify=False)

    def get_vk_id(self, username):
        response = requests.get(
            f"http://127.0.0.1:8005/vk_id/{username}")
        return response
