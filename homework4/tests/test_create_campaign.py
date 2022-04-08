import os
import time
import pytest
from homework4.pages.campaign_page import CampaignPage


@pytest.fixture()
def upload_file_path(repo_root):
    return os.path.join(repo_root, "image_to_upload.jpg")


def test_create_campaign(browser, main_page_fixture, upload_file_path):
    page = CampaignPage(browser)
    time.sleep(4)
    page.fill_data()
    page.upload_file(upload_file_path)
