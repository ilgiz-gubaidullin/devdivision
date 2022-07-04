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
    def prepare(self, browser_final, logger, ui_config_final, repo_root):
        self.repo_root = repo_root
        self.browser = browser_final
        self.base_url: str = SiteData.url
        self.logger: logging.Logger = logger
        self.ui_config: dict = ui_config_final

        self.logger.info('PREPARE DONE')