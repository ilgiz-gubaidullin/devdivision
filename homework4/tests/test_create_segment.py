import time
from homework4.pages.segments_page import SegmentPage


def test_create_segment(browser, main_page_fixture):
    time.sleep(3)
    main_page_fixture.open_segments_page()
    page = SegmentPage(browser)
    page.add_segment()
    page.check_segment_exist()
