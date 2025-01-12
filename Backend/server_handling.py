from database.Database import Database
from models import OpenAIModel
from services import AmadeusService, TripadvisorService
import json


def filter_flights(response_data):
    returned_data = []

    for d in response_data:
        returned_data.append({
            'id': d['id'],
            'itineraries': [itiner['duration'] for itiner in d['itineraries']],
            'price': d['price']['grandTotal'],
        })

    return returned_data[:10]


def filter_hotels(response_data):
    return response_data

def filter_activities(response_data):
    return response_data


def process_response(text_response):
    # print(text_response)
    json_response = json.loads(text_response)
    # print(json_response)

    if json_response['type'] == 'text':
        return {
            'type': 'text',
            'content': json_response['content']
        }

    function_args = json_response['content']['arguments']

    if json_response['content']['name'] == 'analyze_by_criteria':
        db = Database()
        last_data = db.load_latest('responses')
        if len(last_data) == 0:
            return {
                'type': 'text',
                'content': 'Sorry, there is no content to analyze.'
            }
        else:
            last_data = last_data[0]

        filtered_data = None
        if last_data['type'] == 'flights':
            filtered_data = filter_flights(last_data['content']['data'])
        elif last_data['type'] == 'hotels':
            filtered_data = filter_hotels(last_data['content']['data'])
        elif last_data['type'] == 'activities':
            filtered_data = filter_activities(last_data['content']['data'])

        if filtered_data is None:
            return {
                'type': 'text',
                'content': 'Sorry, I cannot analyze the last data.'
            }

        model = OpenAIModel()
        analyze_response = model.analyze(filtered_data, last_data['type'], **function_args)

        # remap data from analyzed response

        output_response = {
            'type': last_data['type'],
            'content': analyze_response
        }

    else:
        svc = AmadeusService()
        svc2 = TripadvisorService()

        # function_lookup = {f['name']: getattr(svc, f['name']) for f in FUNCTIONS}
        function_lookup = {
            'get_flights': svc.get_flights,
            'get_hotels': svc.get_hotels,
            'get_places': svc2.get_places
        }

        function_to_call = function_lookup[json_response['content']['name']]
        function_output = function_to_call(**function_args)

        output_response = {
            'type': json_response['type'],
            'content': function_output
        }

        db = Database()
        db.save('responses', output_response)

    return output_response


if __name__ == '__main__':
    model = OpenAIModel()
    # response = model.invoke('Show me top 5 cheapest flights from Berlin to Paris on 20.01.2025 for 1 adult')
    response = model.invoke('Analyze and give me 5 fastest flights')
    output = process_response(response)
    json.dump(output, open('analyze_flights.json', 'w'))
