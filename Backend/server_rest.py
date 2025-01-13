import yaml
from flask import Flask, request, jsonify
from flask_cors import CORS

from MODEL_ZOO import MODEL_ZOO
from database.Database import Database
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
db = Database()
FAVORITES_COL = 'favorites'


@app.route("/", methods=["GET"])
def home():
    return "Server is running!"

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

@app.route("/favorites", methods=["GET"])
def list_favorites():
    favorites = db.client.collection(FAVORITES_COL).get()
    return jsonify(favorites), 200

@app.route("/favorites", methods=["POST"])
def add_favorite():
    data = request.json
    favorite_data = data.get("item")

    item_id = f"{favorite_data['type']}__{favorite_data['id']}"

    if not favorite_data:
        return jsonify({"error": "Item is required"}), 400

    saved_doc = db.save(FAVORITES_COL, favorite_data, id=item_id)
    return jsonify({"message": "Item added to favorites", "id": saved_doc.id}), 201

@app.route("/favorites/<item_id>", methods=["DELETE"])
def remove_favorite(item_id):
    existing_favorites = db.load(FAVORITES_COL, item_id)
    if not existing_favorites:
        return jsonify({"error": "Item not found"}), 404

    db.delete(FAVORITES_COL, item_id)
    return jsonify({"message": "Item removed from favorites"}), 200

if __name__ == "__main__":
    app.run(config['ENV']['host'], config['ENV']['port'])
