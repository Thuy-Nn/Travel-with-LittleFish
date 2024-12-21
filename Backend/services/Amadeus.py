import yaml
import requests
from pathlib import Path
from datetime import datetime, timedelta
import json


config = yaml.safe_load(open("config.yaml"))


class Amadeus:
    def __init__(self):
        self.api_root = 'https://test.api.amadeus.com/'

    def get_token(self):
        token_file = 'token.json'

        if Path(token_file).exists():
            token_data = json.load(open(token_file))
            expired_at = token_data['expired_at']
            if datetime.now().timestamp() < expired_at:
                return token_data['access_token']

        response = requests.post(self.api_root + 'v1/security/oauth2/token', data={
            'grant_type': 'client_credentials',
            'client_id': config['KEYS']['amadeus_key'],
            'client_secret': config['KEYS']['amadeus_secret'],
        })
        token_data = response.json()
        token_data['expired_at'] = (datetime.now() + timedelta(seconds=token_data['expires_in'])).timestamp()
        print(token_data)
        json.dump(token_data, open(token_file, 'w'))
        return token_data['access_token']

        # {'type': 'amadeusOAuth2Token',
        # 'username': 'amadeus@dttt.io',
        # 'application_name': 'Travel Companion',
        # 'client_id': 'Vjynx6MxNZySZ3k5F7OW5LHWe4F5lBsI',
        # 'token_type': 'Bearer',
        # 'access_token': 'FFBjfAhXBZmUoNK51wqqsayvwyke',
        # 'expires_in': 1799, 'state': 'approved', 'scope': ''}

    def get_flight(self, originLocationCode, destinationLocationCode, departureDate, adults):
        token = self.get_token()

        path = "/v2/shopping/flight-offers"
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "originLocationCode": originLocationCode,
            "destinationLocationCode": destinationLocationCode,
            "departureDate": departureDate,
            "adults": adults
        }
        response = requests.get(self.api_root + path, headers=headers, params=params)
        return response.json()

    def get_hotel(self, city_code):
        token = self.get_token()

        path = "/v1/reference-data/locations/hotels/by-city"
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "city_code": city_code,
        }
        response = requests.get(self.api_root + path, headers=headers, params=params)
        return response.json()


if __name__ == '__main__':
    svc = Amadeus()
    svc.get_token()
    print(svc.token)
