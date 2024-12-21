import yaml
from openai import OpenAI
from models.BaseModel import BaseModel


class OpenAIModel(BaseModel):
    def __init__(self, name):
        super().__init__(name)
        self.config = yaml.safe_load(open('config.yaml'))

    def _load_model(self):
        super()._load_model()
        self.model = OpenAI(api_key=self.config['KEYS']['openai'])

    def _invoke(self, prompt, functions=None):
        response = self.model.chat.completions.create(
            model=self.name,
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
            ],
            # tools=tools
        )

        return response.choices[0].message.content
