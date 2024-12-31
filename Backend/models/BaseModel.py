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

        fn = """{"type": "content_type", content: {"name": "function_name", "arguments": {"arg_1": "value_1", "arg_2": value_2, ...}}}"""

        sys_prompt = f"""You are a helpful assistant with access to the following functions:

        {FUNCTIONS}

        To use these functions respond with:
             {fn} 
             {fn} 
            ...

        Edge cases you must handle:
        - Classify the required response into one of the following types: text, flights, hotels, activities. 
        - If there are no functions that match the user request, you will respond politely that you cannot help.
        - If there is a required argument missing, ask the user to provide the missing argument.
        - If originLocationCode, destinationLocationCode, cityCode are name of city or airport, please convert to IATA code.

        Here is the first prompt: {prompt}

        Please respond with one of the available functions including the arguments. Only return the function with the following 
        format: {fn}. No other text should be included.
        """

        return self._invoke(sys_prompt)

