import allure
import requests
from urllib.parse import urljoin
from requests import HTTPError
from jsonschema import validate
import json
import logging
from json import JSONDecodeError


logger = logging.getLogger("test")


class RequestFailureException(HTTPError, AssertionError):
    pass


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    @staticmethod
    def _logging_pre(url, headers, data, files, expected_status):
        text = f'Performing request:\n' \
               f'URL: {url}\n' \
               f'HEADERS: {headers}\n' \
               f'DATA: {data}\n\n' \
               f'FILES: {files}\n\n' \
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

    def _request(self, method, location, headers=None, params=None, data=None, json_data=None, files=None,
                 check_schema=None, check_status=True, expect_status=200, jsontify=True):
        url = urljoin(self.base_url, location)
        logger.info('-' * 100 + '\n')

        self._logging_pre(url, headers, data or json_data, files, expect_status)

        response = self.session.request(method, url, headers=headers, params=params, data=data, json=json_data,
                                        files=files)

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

        if jsontify:
            return response.json()

        return response

    def post_user_auth(self, email, password):
        r1 = self.session.post(
            "https://auth-ac.my.com/auth",
            data={
                "email": email,
                "password": password,
                "continue": "https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email",
                "failure": "https://account.my.com/login/"
            },
            headers={'Referer': 'https://target.my.com/'},
            params={"lang": "ru", "nosavelogin": "0"})

        cookies = dict(r1.history[0].cookies) | dict(r1.history[4].cookies) | dict(r1.cookies)

        r2 = self.session.get(
            "https://target.my.com/csrf/",
            cookies=cookies)

        csrf_token = dict(r2.cookies)
        self.token = csrf_token['csrftoken']
        return r2

    @allure.step
    def get_segments_list(self):
        location = 'api/v2/remarketing/segments.json'
        params = 'fields=relations__object_type,relations__object_id,relations__params,relations__params__score,relations__id,relations_count,id,name,pass_condition,created,campaign_ids,users,flags&limit=500&_=1651080429165'
        return self._request('GET', location, params=params)

    @allure.step
    def create_segment(self, name_additional):
        location = 'api/v2/remarketing/segments.json'
        headers = {'X-CSRFToken': self.token}
        params = 'fields=relations__object_type,relations__object_id,relations__params,relations__params__score,relations__id,relations_count,id,name,pass_condition,created,campaign_ids,users,flags'
        data = {
                "name": name_additional,
                "pass_condition": 1,
                "relations": [{"object_type": "remarketing_player",
                               "params":{"type": "positive","left": 365,"right": 0}}],
                "logicType": "or"
                }
        response = self._request('POST', location, headers=headers, params=params, json_data=data)
        return response["id"]

    @allure.step
    def delete_segment(self, segment_id):
        location = f'api/v2/remarketing/segments/{segment_id}.json'
        headers = {'X-CSRFToken': self.token}
        return self._request('DELETE', location, headers=headers, expect_status=204, jsontify=False)

    @allure.step
    def submit_url_for_campaign(self, url):
        location = 'api/v1/urls/'
        params = f'url={url}'
        response = self._request('GET', location, params=params)
        return response["id"]

    @allure.step
    def send_image(self, filepath):
        location = 'api/v2/content/static.json'
        headers = {'X-CSRFToken': self.token}
        file = {'file': open(filepath, 'rb')}
        data = {"width": 0, "height": 0}
        response = self._request('POST', location, headers=headers, data=data, files=file)
        return response['id']

    @allure.step
    def get_campaigns_list(self):
        location = 'api/v2/statistics/campaigns/summary.json'
        return self._request('GET', location)

    @allure.step
    def delete_campaign(self, campaign_id):
        location = f'api/v2/campaigns/{campaign_id}.json'
        headers = {'X-CSRFToken': self.token}
        data = {"status": "deleted"}
        return self._request('POST', location, headers=headers, json_data=data, expect_status=204, jsontify=False)
