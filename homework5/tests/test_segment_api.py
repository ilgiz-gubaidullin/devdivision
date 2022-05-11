import pytest
from homework5.base import BaseAPISuiteTest


class TestSegmentApi(BaseAPISuiteTest):

    @pytest.mark.API
    def test_create_segment_by_api(self, unique_value):
        created_segment_id = self.api_client.create_segment(unique_value)
        result = self.check_segment_exist(created_segment_id)
        assert result

    @pytest.mark.API
    def test_delete_segment_by_api(self, unique_value):
        created_segment_id = self.api_client.create_segment(unique_value)
        self.api_client.delete_segment(created_segment_id)
        result = self.check_segment_exist(created_segment_id)
        assert not result
