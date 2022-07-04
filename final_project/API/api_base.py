import logging
import allure
import pytest
from final_project.API.api_client import ApiClientFinal
from final_project.helpers.site_data import SiteData
from final_project.helpers.datamanager import DataManager


class BaseAPITest:

    base_url: str
    api_client_final: ApiClientFinal
    logger: logging.Logger

    @pytest.fixture(autouse=True)
    def prepare(self, api_client_final, logger):
        self.base_url = SiteData.url
        self.api_client_final: ApiClientFinal = api_client_final
        self.logger: logging.Logger = logger
        self.data_manager = DataManager()

        self.logger.info('PREPARE DONE')

