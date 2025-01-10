from models import OpenAIModel
from services import AmadeusService, TripadvisorService
import json


def process_response(text_response):
    print(text_response)
    json_response = json.loads(text_response)
    # print(json_response)

    if json_response['type'] == 'text':
        return {
            'type': 'text',
            'content': json_response['content']
        }

    svc = AmadeusService()
    svc2 = TripadvisorService()

    # function_lookup = {f['name']: getattr(svc, f['name']) for f in FUNCTIONS}
    function_lookup = {
        'get_flights': svc.get_flights,
        'get_hotels': svc.get_hotels,
        'get_places': svc2.get_places
    }

    function_to_call = function_lookup[json_response['content']['name']]
    function_args = json_response['content']['arguments']
    function_output = function_to_call(**function_args)

    return {
        'type': json_response['type'],
        'content': function_output
    }


if __name__ == '__main__':
    model = OpenAIModel('gpt-4o-mini-2024-07-18')
    # response = model.invoke('Show me top 5 cheapest flights from Berlin to Paris on 20.01.2025 for 1 adult')
    response = model.invoke('please search flights from berlin to paris from 25.01.2025 to 27.01.2025')
    output = process_response(response)
    json.dump(output, open('flights.json', 'w'))
