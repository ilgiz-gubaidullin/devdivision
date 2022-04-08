import time
import allure
from homework4.pages.segments_page import SegmentPage


def test_delete_segments(browser, main_page_fixture):
    """
    Тест на удаление сегмента
    """
    with allure.step("Открываем директорию сегментов"):
        time.sleep(3)
        main_page_fixture.open_segments_page()
        page = SegmentPage(browser)
    with allure.step("Добавляем сегмент"):
        page.add_segment()
    with allure.step("Удаляем сегменты"):
        page.delete_segments()
        time.sleep(3)
    with allure.step("Проверяем удаление сегмента"):
        page.check_deletion()
