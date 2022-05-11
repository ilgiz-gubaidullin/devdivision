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
    def create_campaign(self, campaign_name, campaign_url, file_path):
        url_id = self.api_client.submit_url_for_campaign(campaign_url)
        image_id = self.api_client.send_image(file_path)

        location = 'api/v2/campaigns.json'
        headers = {'X-CSRFToken': self.api_client.token}
        data = {
          f"name": campaign_name,
          "read_only": False,
          "conversion_funnel_id": None,
          "objective": "traffic",
          "enable_offline_goals": False,
          "targetings": {
            "split_audience": [
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9,
              10
            ],
            "sex": [
              "male",
              "female"
            ],
            "age": {
              "age_list": [
                0,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                26,
                27,
                28,
                29,
                30,
                31,
                32,
                33,
                34,
                35,
                36,
                37,
                38,
                39,
                40,
                41,
                42,
                43,
                44,
                45,
                46,
                47,
                48,
                49,
                50,
                51,
                52,
                53,
                54,
                55,
                56,
                57,
                58,
                59,
                60,
                61,
                62,
                63,
                64,
                65,
                66,
                67,
                68,
                69,
                70,
                71,
                72,
                73,
                74,
                75
              ],
              "expand": True
            },
            "geo": {
              "regions": [
                188
              ]
            },
            "interests_soc_dem": [],
            "segments": [],
            "interests": [],
            "fulltime": {
              "flags": [
                "use_holidays_moving",
                "cross_timezone"
              ],
              "mon": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23
              ],
              "tue": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23
              ],
              "wed": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23
              ],
              "thu": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23
              ],
              "fri": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23
              ],
              "sat": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23
              ],
              "sun": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23
              ]
            },
            "pads": [
              102643
            ],
            "mobile_types": [
              "tablets",
              "smartphones"
            ],
            "mobile_vendors": [],
            "mobile_operators": []
          },
          "age_restrictions": None,
          "date_start": None,
          "date_end": None,
          "autobidding_mode": "second_price_mean",
          "budget_limit_day": "100",
          "budget_limit": "100",
          "mixing": "recommended",
          "utm": None,
          "enable_utm": True,
          "price": "4",
          "max_price": "0",
          "package_id": 961,
          "banners": [
            {
              "urls": {
                "primary": {
                  "id": url_id
                }
              },
              "textblocks": {},
              "content": {
                "image_240x400": {
                  "id": image_id
                }
              },
              "name": ""
            }
          ]
        }
        response = self.api_client._request('POST', location, headers=headers, json_data=data)
        return response['id']

    @allure.step
    def check_campaign_presence(self, campaign_id):
        campaign_list = self.api_client.get_campaigns_list()
        for i in campaign_list['items']:
            if i['id'] == campaign_id:
                return True
