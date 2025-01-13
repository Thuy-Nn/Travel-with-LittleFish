import yaml
from openai import OpenAI
from models.BaseModel import BaseModel


class OpenAIModel(BaseModel):
    def __init__(self, name='gpt-4o-mini-2024-07-18'):
        super().__init__(name)
        self.config = yaml.safe_load(open('config.yaml'))

    def _load_model(self):
        super()._load_model()
        self.model = OpenAI(api_key=self.config['KEYS']['openai'])

    def _invoke(self, prompt, functions=None):
        tools = None
        if functions is not None:
            tools = [{
                "type": "function",
                "function": f
            } for f in functions]

        response = self.model.chat.completions.create(
            model=self.name,
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant that '},
                {'role': 'user', 'content': prompt}
            ],
            tools=tools
        )

        print(response.choices[0].message)

        if response.choices[0].message.tool_calls is None:
            return response.choices[0].message.content
        else:
            tool_calls = response.choices[0].message.tool_calls[0]
            return {
                'function_name': tool_calls.function.name,
                'function_arguments': tool_calls.function.arguments,
            }
