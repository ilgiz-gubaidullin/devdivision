import pytest
from final_project.helpers.site_data import SiteData
from final_project.API.client import ApiClientFinal


@pytest.fixture(scope='session')
def api_client_final():
    client = ApiClientFinal(SiteData.url)
    client.post_user_auth(SiteData.main_user, SiteData.main_user_pass)
    return client
