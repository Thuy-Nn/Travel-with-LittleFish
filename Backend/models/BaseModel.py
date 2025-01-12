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

        fn = """{"type": "content_type", "content": {"name": "function_name", "arguments": {"arg_1": "value_1", "arg_2": value_2, ...}}}"""

        if prompt.startswith('Analyze'):
            functions = FUNCTIONS['UTILS']
            guide_text = """
            - For the function "get_criteria", the "sortBy" can only be "price", "duration", or "distance". And the "sortOrder" can only be "ascending", or "descending".
            """
        else:
            functions = FUNCTIONS['API']
            guide_text = """
            - If originLocationCode, destinationLocationCode, cityCode are name of city or airport, please convert to IATA code.
            - For the function "get_places", the category can only be "hotels", "restaurants", or "attractions".
            """

        sys_prompt = f"""You are a helpful assistant with access to the following functions:

        {functions}

        To use these functions respond with:
             {fn} 
             {fn} 
            ...

        Edge cases you must handle:
        - Classify the required response into one of the following types: text, flights, hotels, activities.
        - For the "text" response, "content" should include the text only.
        - If there are no functions that match the user request, you will respond politely that you cannot help.
        - If there is a required argument missing, ask the user to provide the missing argument.         
        {guide_text}

        Here is the first prompt: {prompt}

        Please respond with one of the available functions including the arguments. Only return the function with the following 
        format: {fn}. No other text should be included.
        """

        return self._invoke(sys_prompt)

    def analyze(self, response, type, sortBy, sortOrder=None):
        # print(f'Analyze by {sortBy} {sortOrder}')

        if self.model is None:
            self._load_model()

        prompt = f"""Given the JSON below which is a list of {type}, each contains an id. 
        Sort the items in the JSON by {sortBy} {sortOrder}. Only return the list of ids. No other text should be included.
        {response}
        """

        return self._invoke(prompt)

