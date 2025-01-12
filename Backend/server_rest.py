import yaml
from flask import Flask, request, jsonify
from flask_cors import CORS

from database import Database

from MODEL_ZOO import MODEL_ZOO
from server_handling import process_response

config = yaml.safe_load(open("config.yaml"))

app = Flask(__name__)
CORS(app)

# Load the model and tokenizer
MODEL_TYPE = "OpenAI"
MODEL_NAME = "gpt-4o-mini-2024-07-18"
# MODEL_TYPE = "Llama"
# MODEL_NAME = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
# MODEL_TYPE = "Qwen"
# MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

model = None

# chroma_client = chromadb.PersistentClient(path="database/chromadb")
# collection = chroma_client.get_or_create_collection(name="sent_emails_anonymized")

# API endpoint for chatbot
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    global model
    if model is None:
        if MODEL_TYPE not in MODEL_ZOO:
            return jsonify({"error": "Model type is not supported"}), 400
        model = MODEL_ZOO[MODEL_TYPE](MODEL_NAME)

    if model is None:
        return jsonify({"error": "Internal server error"}), 500

    response = model.invoke(user_message)
    output = process_response(response)

    return jsonify(output)

@app.route("/", methods=["GET"])
def home():
    return "Server is running!"


if __name__ == "__main__":
    app.run(config['ENV']['host'], config['ENV']['port'])
