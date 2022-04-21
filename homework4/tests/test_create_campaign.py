import os
import allure
import pytest


@pytest.fixture()
def upload_file_path(repo_root):
    return os.path.join(repo_root, "image_to_upload.jpg")


def test_create_campaign(browser, main_page_fixture, upload_file_path, unique_value):
    """
    Тест проверяет создание компании
    """
    with allure.step("Открываем директорию кампаний"):
        page = main_page_fixture.open_campaign_page()
    with allure.step("Заполняем данные"):
        page.fill_data(unique_value)
    with allure.step("Загружаем фото"):
        page.upload_file(upload_file_path)
    with allure.step("Проверяем создание кампании"):
        page.check_campaign_created(unique_value)
