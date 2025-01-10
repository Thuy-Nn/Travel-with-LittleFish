import requests
import yaml
import json

config = yaml.safe_load(open("config.yaml"))

'''
Go to Google Cloud Console and enable these APIs:
- Places API
- Places API (New)
- Geocoding API
- Maps Embed API
'''


class GooglePlaceService:
    def __init__(self):
        self.api_key = config["KEYS"]["maps_embed"]
        self.api_root = "https://maps.googleapis.com/maps/api/"

    def get_place_id(self, latitude, longitude, hotel_name):
        # hotel_name = 'HOTEL VILLA PANTHEON'
        # lat_lng = '48.84917,2.34615'
        lat_lng = f'{latitude},{longitude}'
        path = 'place/textsearch/json'
        params = '?location=' + lat_lng + '&query=' + hotel_name + '&radius=10&key='
        url = self.api_root + path + params + self.api_key

        response = requests.request('GET', url, data={})
        json_response = json.loads(response.text)
        first_item = json_response['results'][0]
        place_id = first_item['place_id']
        photo_reference = first_item['photos'][0]['photo_reference']
        return place_id, photo_reference

    def get_place_photos(self, photo_reference):
        url = self.api_root + 'place/photo?photo_reference=' + photo_reference + '&key=' + self.api_key + '&maxwidth=400'
        photo_url = requests.Request('GET', url).prepare().url
        return photo_url

    def get_hotel_photos(self, latitude, longitude, hotel_name):
        try:
            place_id, photo_reference = self.get_place_id(latitude, longitude, hotel_name)
            photo_url = self.get_place_photos(photo_reference)
            return photo_url
        except Exception as e:
            print('Error getting images:', e)
        return ''
