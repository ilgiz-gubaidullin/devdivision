import pytest
from final_project.UI.ui_base import BaseUISuiteTest


class TestMainPageUI(BaseUISuiteTest):

    @pytest.mark.debug
    def test_login(browser):
        browser.get('https://ya.ru')
        assert browser.current_url == 'https://ya.ru/'