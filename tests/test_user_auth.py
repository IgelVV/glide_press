import requests


BASE_URL = 'https://auth.glide.press'
DEFAULT_TOKEN = {
  "bearer": (
      "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
      "eyJ1c2VyX2lkIjoiNjM0OTc2YWIwZTYwMjk2NzMyZDVlYjhhIiwiZXhwaXJlcyI6MTY2NjE4MTI0OC4xMzY5MTc4fQ."
      "6RhHBC1ZdwNMlZyGWltYufIGOEOfbw5j9iui_MIM-eM"
  ),
  "expires": 1666181248.1369178
}


class TestUserAuth:
    headers = {
        'accept': 'application/json',
        'social-type': '1'
    }

    def test_registration(self):
        response = requests.post(BASE_URL + '/registration', headers=self.headers)
        assert response.status_code == 200

    def test_auth(self):
        response = requests.get(BASE_URL + '/auth', headers=self.headers)
        assert response.status_code == 200

    # /verify always returns 200 yet
    def test_verify(self):
        headers = {
            'accept': 'application/json',
            "bearer": DEFAULT_TOKEN["bearer"]
        }
        response = requests.get(BASE_URL + '/verify', headers=headers)
        assert response.status_code == 200
        headers2 = {
            'accept': 'application/json',
            "bearer": 'Random'
        }
        response2 = requests.get(BASE_URL + '/verify', headers=headers2)
        assert response2.status_code != 200

    # /refresh always returns 500
    def test_refresh(self):
        headers = {
            'accept': 'application/json',
            "bearer": DEFAULT_TOKEN["bearer"]
        }

        response = requests.get(BASE_URL + '/refresh', headers=headers)
        assert response.status_code == 200
        headers2 = {
            'accept': 'application/json',
            "bearer": 'Random'
        }
        response2 = requests.get(BASE_URL + '/refresh', headers=headers2)
        assert response2.status_code != 200
