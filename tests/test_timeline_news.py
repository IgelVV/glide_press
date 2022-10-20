import requests
import pytest
import json

BASE_URL = 'https://api.glide.press'


class TestTimelineNews:
    timeline_url = BASE_URL + '/timelines'
    headers = {'accept': 'application/json'}

    @pytest.fixture(scope='function')
    def params(self):
        params = {
            'tag_id': '',
            'skip': '0',
            'limit': '10',
            'expand_tags': 'false',
            'expand_user': 'false'
        }
        return params

    @pytest.mark.parametrize('endpoint', ['/in-focus', '/global-lowdown'])
    def test_timeline_in_focus(self, endpoint, params):
        response = requests.get(
            self.timeline_url + endpoint,
            headers=self.headers,
            params=params
        )
        assert response.status_code == 200

    @pytest.mark.parametrize(
        'endpoint, limit',
        [('/in-focus', 2), ('/global-lowdown', 1)]
    )
    def test_timeline_in_focus_limit(self, params, endpoint, limit):
        params['limit'] = str(limit)
        response = requests.get(
            self.timeline_url + endpoint,
            headers=self.headers,
            params=params
        )
        assert len(json.loads(response.text)) <= limit
