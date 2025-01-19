import json

from database.Database import Database
from models import OpenAIModel
from services import AmadeusService, TripadvisorService
from utils.time import iso8601_to_minutes


def filter_flights(response_data, limit=10):
    returned_data = []

    for d in response_data:
        filter_item = {
            'id': d['id'],
            'price': d['price']['grandTotal'],
            'durationInMinutes': 0,
            'numberOfStops': 0
        }

        for itiner in d['itineraries']:
            filter_item['durationInMinutes'] += iso8601_to_minutes(itiner['duration'])
            for seg in itiner['segments']:
                filter_item['numberOfStops'] += seg['numberOfStops']

        returned_data.append(filter_item)

    return returned_data[:limit]


def filter_hotels(response_data, limit=10):
    returned_data = []

    for d in response_data:
        item = {
            'id': d['id'],
            'distance': d['distance'],
            'price': d['offer']['price']['total'],
        }

        if 'overallRating' in d:
            item['rating'] = d['overallRating']

        returned_data.append(item)  # ham gan, bo sung item them vao

    return returned_data[:limit]


def filter_activities(response_data, limit=10):
    returned_data = []

    for d in response_data:
        returned_data.append({
            'id': d['id'],
            'rating': d['rating'],
        })
    return returned_data[:limit]


def process_response(llm_response):
    # print(llm_response)

    if 'function_name' not in llm_response:
        return {
            'type': 'text',
            'content': llm_response,
        }

    if 'function_arguments' in llm_response:
        function_args = json.loads(llm_response['function_arguments'])
        # print(function_args)

    if llm_response['function_name'] == 'analyze_by_criteria':
        db = Database()
        last_data = db.load_latest('responses', function_args['content_type'])
        if len(last_data) == 0:
            return {
                'type': 'text',
                'content': 'Sorry, there is no content to analyze.'
            }
        else:
            last_data = last_data[0]

        print('Analyze the last data:', last_data['created_at'])

        filtered_data = None
        if last_data['type'] == 'flights':
            filtered_data = filter_flights(last_data['content']['data'], limit=50)
        elif last_data['type'] == 'hotels':
            filtered_data = filter_hotels(last_data['content'], limit=50)
        elif last_data['type'] in ['attractions', 'restaurants']:
            filtered_data = filter_activities(last_data['content'], limit=50)

        if filtered_data is None:
            return {
                'type': 'text',
                'content': 'Sorry, I cannot analyze the last data.'
            }

        model = OpenAIModel()
        analyzed_ids = model.analyze(filtered_data, **function_args)

        if last_data['type'] == 'flights':
            analyzed_response = {
                **last_data['content'],
                'data': []
            }
            id_map = {}
            for d in last_data['content']['data']:
                id_map[d['id']] = d
            for id in analyzed_ids:
                analyzed_response['data'].append(id_map[id])

        elif last_data['type'] == 'hotels':
            analyzed_response = []
            id_map = {}
            for d in last_data['content']:
                id_map[d['id']] = d
            for id in analyzed_ids:
                analyzed_response.append(id_map[id])

        elif last_data['type'] in ['attractions', 'restaurants']:
            analyzed_response = []
            id_map = {}
            for d in last_data['content']:
                id_map[d['id']] = d
            for id in analyzed_ids:
                analyzed_response.append(id_map[id])

        output_response = {
            'type': last_data['type'],
            'content': analyzed_response
        }

    else:
        svc = AmadeusService()
        svc2 = TripadvisorService()

        # function_lookup = {f['name']: getattr(svc, f['name']) for f in FUNCTIONS}
        function_lookup = {
            'get_flights': {
                'type': 'flights',
                'function': svc.get_flights
            },
            'get_hotels': {
                'type': 'hotels',
                'function': svc.get_hotels
            },
            'get_places': {
                'type': None,  # should be replaced by the content category after receiving the response
                'function': svc2.get_places
            }
        }

        # print("llm_response:", llm_response['function_name'])
        function_to_call = function_lookup[llm_response['function_name']]
        # print("function_to_call", function_to_call)
        function_output = function_to_call['function'](**function_args)
        # print("function_to_call['function']:", function_to_call['function'])

        print(function_to_call)
        print(function_output)

        if 'error_at' in function_output:
            return {
                'type': 'error',
                'content': json.dumps(function_output)
            }

        if llm_response['function_name'] == 'get_places':
            function_to_call['type'] = function_args['category']

        if llm_response['function_name'] in ['get_hotels', 'get_places']:
            function_output = [{
                'id': k,
                **v  # copy v
            } for k, v in function_output.items()]

        output_response = {
            'type': function_to_call['type'],
            'content': function_output
        }

        db = Database()
        db.save('responses', output_response)

    return output_response


if __name__ == '__main__':
    model = OpenAIModel()
    # # response = model.invoke('Hi')
    # response = model.invoke('Show me top 5 cheapest flights from Berlin to Paris on 20.01.2025 for 1 adult')
    # response = model.invoke('Show me top hotels in paris from 25.01.2025 to 27.01.2025')
    # response = model.invoke('Analyze top 1 cheapest hotels')
    # response = model.invoke('Hotels in Hanoi from 20.02 to 24.02.2025 for 1 adult')
    # response = model.invoke('show me attractions in Seoul')
    response = model.invoke('Analyze top 3 best flights')
    output = process_response(response)
    json.dump(output, open('output/analyze.json', 'w'))
