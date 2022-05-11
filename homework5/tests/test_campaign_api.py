import pytest
from homework5.base import BaseAPISuiteTest


class TestCampaignApi(BaseAPISuiteTest):

    @pytest.mark.API
    def test_create_campaign_by_api(self, unique_value, upload_file_path, fake_email):
        campaign_id = self.create_campaign(campaign_name=unique_value, campaign_url=fake_email, file_path=upload_file_path)
        assert self.check_campaign_presence(campaign_id)
        self.api_client.delete_campaign(campaign_id)
