from models import QwenModel
from models import OpenAIModel, LlamaModel

MODEL_ZOO = {
    "Qwen": QwenModel,
    "OpenAI": OpenAIModel,
    "Llama": LlamaModel
}