import yaml
# from openai import OpenAI
from models.BaseModel import BaseModel
from openai import AzureOpenAI


class OpenAIModel(BaseModel):
    def __init__(self, name='gpt-4o'):
        super().__init__(name)
        self.config = yaml.safe_load(open('config.yaml'))

    def _load_model(self):
        super()._load_model()
        # self.model = OpenAI(api_key=self.config['KEYS']['openai'])
        endpoint = self.config['KEYS']['azure_openai_endpoint']
        key = self.config['KEYS']['azure_openai_key']
        api_version = '2023-07-01-preview'  # gpt-4o
        # api_version = '2024-09-12' # gpt-o1-mini
        self.client = AzureOpenAI(azure_endpoint=endpoint, api_key=key, api_version=api_version)

    def _invoke(self, prompt, functions=None):
        tools = None
        if functions is not None:
            tools = [{
                "type": "function",
                "function": f
            } for f in functions]

        response = self.client.chat.completions.create(
            model=self.name,
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant that '},
                {'role': 'user', 'content': prompt}
            ],
            tools=tools
        )

        # print(response.choices[0].message)

        if response.choices[0].message.tool_calls is None:
            return response.choices[0].message.content
        else:
            tool_calls = response.choices[0].message.tool_calls[0]
            return {
                'function_name': tool_calls.function.name,
                'function_arguments': tool_calls.function.arguments,
            }
