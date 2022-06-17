import logging
import pytest
import typing
from final_project.UI.pages.base_page import BasePage
from final_project.helpers.site_data import SiteData


T = typing.TypeVar('T', bound=BasePage)


class BaseUISuiteTest:

    base_url: str
    logger: logging.Logger
    ui_config: dict

    @pytest.fixture(autouse=True)
    def prepare(self, browser, logger, ui_config, repo_root):
        self.repo_root = repo_root
        self.browser = browser
        self.base_url: str = SiteData.url
        self.logger: logging.Logger = logger
        self.ui_config: dict = ui_config

        self.logger.info('PREPARE DONE')