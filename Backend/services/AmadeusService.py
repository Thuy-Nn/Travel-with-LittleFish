import yaml
import requests
from pathlib import Path
from datetime import datetime, timedelta
import json

from services.GooglePlaceService import GooglePlaceService

config = yaml.safe_load(open("config.yaml"))


class AmadeusService:
    def __init__(self):
        self.api_root = 'https://api.amadeus.com/'
        self.google_service = GooglePlaceService()

    def _get_token(self):
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
        # print(token_data)
        json.dump(token_data, open(token_file, 'w'))
        return token_data['access_token']

    def get_flights(self, originLocationCode, destinationLocationCode, departureDate, adults=1,
                    returnDate=None, travelClass='ECONOMY', nonStop=False, currencyCode='VND', max=20
                    ):
        token = self._get_token()

        path = "/v2/shopping/flight-offers"
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "originLocationCode": originLocationCode,
            "destinationLocationCode": destinationLocationCode,
            "departureDate": departureDate,
            "adults": adults,
            "returnDate": returnDate,
            # "travelClass": travelClass,
            # "nonStop": nonStop,
            # "currencyCode": currencyCode,
            "max": max
        }
        response = requests.get(self.api_root + path, headers=headers, params=params)
        # process something
        return response.json()

    def _get_hotel_listing(self, cityCode, radius=1, ratings=None):
        token = self._get_token()

        path = "/v1/reference-data/locations/hotels/by-city"
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "cityCode": cityCode,
            "radius": radius,
            "radiusUnit": "KM",
            "ratings": ratings
        }
        response = requests.get(self.api_root + path, headers=headers, params=params)
        return response.json()

    def _get_hotel_price(self, hotelIds, checkInDate, checkOutDate, adults=1, bestRateOnly=True):
        token = self._get_token()

        path = "/v3/shopping/hotel-offers"
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "hotelIds": ','.join(hotelIds),
            "checkInDate": checkInDate,
            "checkOutDate": checkOutDate,
            "adults": adults,
            "bestRateOnly": bestRateOnly
        }
        response = requests.get(self.api_root + path, headers=headers, params=params)
        return response.json()

    def _get_hotel_ratings(self, hotelIds):
        token = self._get_token()

        path = "/v2/e-reputation/hotel-sentiments"
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "hotelIds": ','.join(hotelIds)
        }
        response = requests.get(self.api_root + path, headers=headers, params=params)
        return response.json()

    def get_hotels(self, cityCode, checkInDate, checkOutDate, adults=1, radius=3, ratings=None):
        hotel_listing = self._get_hotel_listing(cityCode, radius, ratings)

        if 'data' not in hotel_listing:
            return {
                'error_at': 'hotel_listing',
                'details': hotel_listing
            }

        hotel_listing['data'] = hotel_listing['data'][:10]  # max 50
        print('Hotels found:', hotel_listing['meta']['count'])

        hotel_ids = []
        hotel_listing_map = {}
        for h in hotel_listing['data']:
            hotel_ids.append(h['hotelId'])
            hotel_listing_map[h['hotelId']] = h

        # print(hotel_ids)

        hotel_price = self._get_hotel_price(hotel_ids, checkInDate, checkOutDate, adults)

        if 'data' not in hotel_price:
            return {
                'error_at': 'hotel_price',
                'details': hotel_price
            }

        hotel_price_ids = []
        hotel_price_map = {}
        for h in hotel_price['data']:
            hotel_price_ids.append(h['hotel']['hotelId'])
            hotel_price_map[h['hotel']['hotelId']] = h

        # print(hotel_price_ids)

        hotel_ratings_map = {}
        for i in range(0, len(hotel_price_ids), 3):
            hids = hotel_price_ids[i: i + 3]
            ratings = self._get_hotel_ratings(hids)
            if 'data' in ratings:
                for h in ratings['data']:
                    hotel_ratings_map[h['hotelId']] = h

        selected_hotels = {}

        for hid in hotel_price_ids:
            selected_hotels[hid] = {
                'name': hotel_listing_map[hid]['name'],
                'geoCode': hotel_listing_map[hid]['geoCode'],
                'distance': hotel_listing_map[hid]['distance'],
                'offer': hotel_price_map[hid]['offers'][0],
            }

            if hid in hotel_ratings_map:
                # bo sung data, neu viet theo format ben tren, data gan moi va data gan cu se mat
                selected_hotels[hid]['numberOfRatings'] = hotel_ratings_map[hid]['numberOfRatings']
                selected_hotels[hid]['overallRating'] = hotel_ratings_map[hid]['overallRating']
                selected_hotels[hid]['image'] = self.google_service.get_hotel_photos(
                    selected_hotels[hid]['geoCode']['latitude'], selected_hotels[hid]['geoCode']['longitude'],
                    selected_hotels[hid]['name'])

        return selected_hotels
