import time
import allure
from homework4.pages.segments_page import SegmentPage


def test_create_segment(browser, main_page_fixture):
    """
    Тест на создание сегмента
    """
    with allure.step("Открываем директорию сегментов"):
        time.sleep(3)
        main_page_fixture.open_segments_page()
        page = SegmentPage(browser)
    with allure.step("Добавляем сегмент"):
        page.add_segment()
    with allure.step("Проверяем сегмент"):
        page.check_segment_exist()
