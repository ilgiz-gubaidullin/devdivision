import allure
from homework5.client import ApiClient


def test_delete_segments(browser, api_client, main_page_fixture, unique_value):
    """
    Тест на удаление сегмента
    """
    with allure.step("Открываем директорию сегментов"):
        page = main_page_fixture.open_segments_page()
    with allure.step("Добавляем сегмент"):
        api_client.create_segment(unique_value)
    with allure.step("Удаляем сегмент"):
        page.delete_segment(unique_value)
    with allure.step("Проверяем удаление сегмента"):
        browser.refresh()
        page.check_deletion(unique_value)
