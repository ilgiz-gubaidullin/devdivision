import logging
import allure
import pytest
from homework5.client import ApiClient


class BaseAPISuiteTest:

    base_url: str
    api_client: ApiClient
    logger: logging.Logger

    @pytest.fixture(autouse=True)
    def prepare(self, api_client, logger):
        self.base_url = "https://target.my.com/"
        self.api_client: ApiClient = api_client
        self.logger: logging.Logger = logger

        self.logger.info('PREPARE DONE')

    @allure.step
    def check_segment_exist(self, segment_id):
        segments_list = self.api_client.get_segments_list()
        for i in range(int(segments_list['count'])):
            if segments_list['items'][i]['id'] == segment_id:
                return True

    @allure.step
    def check_campaign_presence(self, campaign_id):
        campaign_list = self.api_client.get_campaigns_list()
        for i in campaign_list['items']:
            if i['id'] == campaign_id:
                return True
