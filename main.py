import requests
import pytest


url = 'https://auth.glide.press/registration'
headers = {
    'accept': 'application/json',
    'social-type': '1'
}

data = {}

r = requests.post(url, headers=headers)
print(r.status_code)
print(r.text)