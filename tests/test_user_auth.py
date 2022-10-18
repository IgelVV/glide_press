import requests


base_url = 'https://auth.glide.press'
# url_reg = 'https://auth.glide.press/registration'
# url_verify = 'https://auth.glide.press/verify'
default_token = {
  "bearer": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjM0OTc2YWIwZTYwMjk2NzMyZDVlYjhhIiwiZXhwaXJlcyI6MTY2NjE4MTI0OC4xMzY5MTc4fQ.6RhHBC1ZdwNMlZyGWltYufIGOEOfbw5j9iui_MIM-eM",
  "expires": 1666181248.1369178
}


def test_registration():
    headers = {
        'accept': 'application/json',
        'social-type': '1'
    }

    response = requests.post(base_url+'/registration', headers=headers)
    assert response.status_code == 200


def test_auth():
    headers = {
        'accept': 'application/json',
        'social-type': '1'
    }

    response = requests.get(base_url+'/auth', headers=headers)
    assert response.status_code == 200


# /verify always returns 200 yet
def test_verify():
    headers = {
        'accept': 'application/json',
        "bearer": default_token["bearer"]
    }
    response = requests.get(base_url+'/verify',  headers=headers)
    assert response.status_code == 200
    headers2 = {
        'accept': 'application/json',
        "bearer": 'Random'
    }
    response2 = requests.get(base_url+'/verify',  headers=headers2)
    assert response2.status_code != 200


# /refresh always returns 500
def test_refresh():
    headers = {
        'accept': 'application/json',
        "bearer": default_token["bearer"]
    }

    response = requests.get(base_url + '/refresh', headers=headers)
    assert response.status_code == 200
    headers2 = {
        'accept': 'application/json',
        "bearer": 'Random'
    }
    response2 = requests.get(base_url + '/refresh', headers=headers2)
    assert response2.status_code != 200

