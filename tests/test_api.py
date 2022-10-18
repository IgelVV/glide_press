import requests
import pytest
import json
import random

base_url = 'https://api.glide.press'


class TestTimelineNews:
    timeline_url = base_url + '/timelines'
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


class TestArticle:
    articles_url = base_url + '/articles'

    headers = {
        'accept': 'application/json'
    }

    params = {
        'expand_tags': 'false',
        'expand_user': 'false'
    }

    article_id = ''

    def create_new_article(self):
        data = {
            "title": f"About cinema{random.randint(1, 10000000)}",
            "summary": "films",
            "text": "Long read article. Long read article",
            "tags": [
                {
                    "title": "Cinema",
                    "image_url": ""
                }
            ],
            "image_url": ""
        }
        headers = {
            'accept': 'application/json',
            'Content - Type': 'application / json'
        }
        response = requests.post(
            self.articles_url,
            headers=headers,
            data=json.dumps(data)
        )
        return response

    def publish_article(self, artcl_id):
        response = requests.put(
            self.articles_url + f'/{artcl_id}/publish',
            headers=self.headers
        )
        return response

    def get_article(self, artcl_id):
        response = requests.get(
            self.articles_url+f'/{artcl_id}',
            params=self.params,
            headers=self.headers
        )
        return response

    def delete_article(self, artcl_id):
        response = requests.delete(
            self.articles_url + f'/{artcl_id}',
            headers=self.headers
        )
        return response

    def test_create_publish_and_delete_article(self):
        new_article = self.create_new_article()
        assert new_article.status_code == 200

        self.article_id = json.loads(new_article.text)['id']
        published_article = self.publish_article(self.article_id)
        assert published_article.status_code == 200
        assert json.loads(published_article.text)['id'] == self.article_id

        article = self.get_article(self.article_id)
        assert article.status_code == 200
        assert json.loads(article.text)['id'] == self.article_id

        response_del = self.delete_article(self.article_id)
        assert response_del.status_code == 200
        assert 'deleted' in json.loads(response_del.text)['message'].lower()

        response_get = self.get_article(self.article_id)
        assert response_get.status_code == 404
        assert 'not found' in json.loads(response_get.text)['detail'].lower()

