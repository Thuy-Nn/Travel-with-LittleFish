class BaseModel:
    def __init__(self, name):
        self.name = name
        self.model = None
        self.tokenizer = None

    def _load_model(self):
        print(f"Model {self.name} is loaded")
        pass

    def _invoke(self, prompt):
        pass

    def invoke(self, prompt):
        if self.model is None:
            self._load_model()

        return self._invoke(prompt)