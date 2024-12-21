from gpt4all import GPT4All
from models.BaseModel import BaseModel

class LlamaModel(BaseModel):
    def __init__(self, name):
        super().__init__(name)

    def _load_model(self):
        super()._load_model()
        self.model = GPT4All(self.name)

    def _invoke(self, prompt):
        output = self.model.generate("<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n" + prompt +
                        "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n", max_tokens=1000, temp=0.6)

        return output

