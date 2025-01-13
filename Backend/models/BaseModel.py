from services import FUNCTIONS
import ast


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
        """

        return self._invoke(sys_prompt, functions)

    def analyze(self, response, content_type, sort_by, sort_order=None, limit=10):
        if self.model is None:
            self._load_model()

        prompt = f"""Given the JSON below which is a list of {content_type}, each contains an id. 
        Sort the items in the JSON by {sort_by} {sort_order}. Only return the list of ids. The most important that no other text should be included.
        If there is a required argument missing, ask the user to provide the missing argument.
        {response}
        """

        analyzed_ids = self._invoke(prompt)

        # trim unnecessary text
        pos1 = analyzed_ids.find('[')
        pos2 = analyzed_ids.rfind(']')
        if -1 < pos1 < pos2:
            analyzed_ids = analyzed_ids[pos1:pos2 + 1]

        parsed_ids = ast.literal_eval(analyzed_ids)

        return parsed_ids[:limit]
        # return parsed_ids
