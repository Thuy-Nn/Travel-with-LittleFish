import json

from services import FUNCTIONS


class BaseModel:
    def __init__(self, name):
        self.name = name
        self.model = None
        self.tokenizer = None

    def _load_model(self):
        print(f"Model {self.name} is loaded")
        pass

    def _invoke(self, prompt, tools=None):
        pass

    def invoke(self, prompt):
        if self.model is None:
            self._load_model()

        # return self._invoke(prompt)

        if prompt.startswith('Analyze') or prompt.startswith('analyze'):
            functions = FUNCTIONS['UTILS']
        else:
            functions = FUNCTIONS['API']

        sys_prompt = f"""{prompt}
        Edge cases you must handle:
        - If there are no functions that match the user request, you will respond politely that you cannot help.
        - If a required argument is missing, prompt the user to provide it. This step is crucial.
        - If the dates are in the past, prompt the user to provide an updated date. This step is crucial.
        """

        return self._invoke(sys_prompt, functions)

    def analyze(self, response, content_type, sort_by, sort_order=None, limit=10):
        if self.model is None:
            self._load_model()

        if content_type == 'flights' and sort_by == 'best_value':
            guide_text = f'''
            Sort items in the list by the combination of "price", "duration", and "number of stops" with the corresponding weights are [0.5, 0.3, 0.2].
            The sorting order is {sort_order}.
            '''
        else:
            guide_text = f"Sort items in the list by {sort_by} {sort_order}."

        # opinion_guide_text = 'For each item, provide your opinion about it in 1-2 sentences. Your opinion might be either positive or negative.'

        prompt = f"""Given the list below which is a list of {content_type}, each contains an id and other information. 
        {guide_text}        
        Only return a JSON string which contains list of ids sorted by the criteria mentioned above. No other text should be included.
        If there is a required argument missing, ask the user to provide the missing argument.
        Here is the list:
        {response}
        """

        analyzed_response = self._invoke(prompt)

        # trim unnecessary text
        pos1 = analyzed_response.find('[')
        pos2 = analyzed_response.rfind(']')
        if -1 < pos1 < pos2:
            analyzed_response = analyzed_response[pos1:pos2 + 1]

        parsed_response = json.loads(analyzed_response)

        return parsed_response[:limit]
