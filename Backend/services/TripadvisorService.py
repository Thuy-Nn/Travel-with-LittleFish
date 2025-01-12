import requests
import yaml

config = yaml.safe_load(open("config.yaml"))

class TripadvisorService:
    def __init__(self):
        self.api_root = 'https://api.content.tripadvisor.com/api/'
        self.key = config['KEYS']['tripadvisor']

    def get_location(self, searchQuery, category):

        path = 'v1/location/search'
        params = {
            'searchQuery': searchQuery,
            'category': category,
            'key': self.key
        }

        response = requests.get(self.api_root + path, params=params)
        return response.json()

    def get_location_details(self, locationId):

        path = f'v1/location/{locationId}/details'
        params = {
            'key': self.key
        }

        response = requests.get(self.api_root + path, params=params)
        return response.json()

    def get_location_photos(self, locationId):
        path = f'v1/location/{locationId}/photos'
        params = {
            'key': self.key
        }
        response = requests.get(self.api_root + path, params=params)
        return response.json()

    def get_places(self, searchQuery, category):
        location_listing = self.get_location(searchQuery, category)
        # print(location_listing)

        if 'database' not in location_listing:
            return{
                'error_at': 'location not found',
                'details': location_listing
            }

        location_ids = []
        location_listing_map = {}
        for lid in location_listing['database']:
            location_ids.append(lid['location_id'])
            location_listing_map[lid['location_id']] = lid

        # location_details = self.get_location_details(location_ids)

        location_details_map = {}
        for l in location_ids:
            location_details = self.get_location_details(l)
            location_details_map[l] = location_details

        location_photos_map = {}
        for l in location_ids:
            location_photos = self.get_location_photos(l)
            location_photos_map[l] = location_photos

        # import json
        # json.dump(location_details_map, open('location_details.json', 'w'))

        selected_locations = {}

        for lid in location_ids:
            selected_locations[lid] = {
                'name': location_listing_map[lid]['name'],
                'address': location_listing_map[lid]['address_obj']['address_string'],
            }

            if lid in location_details_map:
                if 'latitude' in location_details_map[lid]:
                    selected_locations[lid]['latitude'] = location_details_map[lid]['latitude']
                if 'longitude' in location_details_map[lid]:
                    selected_locations[lid]['longitude'] = location_details_map[lid]['longitude']
                if 'ranking' in location_details_map[lid]:
                    selected_locations[lid]['ranking'] = location_details_map[lid]['ranking_data']
                if 'rating' in location_details_map[lid]:
                    selected_locations[lid]['rating'] = location_details_map[lid]['rating']
                if 'hours' in location_details_map[lid]:
                    selected_locations[lid]['weekday_text'] = location_details_map[lid]['hours']['weekday_text']

            if lid in location_photos_map:
                if 'database' in location_photos_map[lid]:
                    selected_locations[lid]['images'] = location_photos_map[lid]['database'][0]['images']['large']['url']

        return selected_locations





