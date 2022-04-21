import allure


def test_create_segment(browser, main_page_fixture, unique_value):
    """
    Тест на создание сегмента
    """
    with allure.step("Открываем директорию сегментов"):
        page = main_page_fixture.open_segments_page()
    with allure.step("Добавляем сегмент"):
        page.add_segment(unique_value)
    with allure.step("Проверяем сегмент"):
        page.check_segment_exist(unique_value)
