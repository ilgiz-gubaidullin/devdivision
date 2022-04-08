import os
import time

import allure
import pytest
from homework4.pages.campaign_page import CampaignPage


@pytest.fixture()
def upload_file_path(repo_root):
    return os.path.join(repo_root, "image_to_upload.jpg")


def test_create_campaign(browser, main_page_fixture, upload_file_path):
    """
    Тест проверяет создание компании
    """
    with allure.step("Открываем директорию кампаний"):
        page = CampaignPage(browser)
        time.sleep(4)

    with allure.step("Заполняем данные"):
        page.fill_data()
    with allure.step("Загружаем фото"):
        page.upload_file(upload_file_path)
        time.sleep(5)
    with allure.step("Проверяем создание кампании"):
        page.check_campaign_created()
