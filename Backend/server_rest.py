from flask import Flask, request, jsonify
from MODEL_ZOO import MODEL_ZOO


app = Flask(__name__)

# Load the model and tokenizer
MODEL_TYPE = 'Qwen'
MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
model = None


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

    return jsonify({"response": response})

@app.route("/", methods=["GET"])
def home():
    return "Server is running!"


if __name__ == "__main__":
    app.run(debug=True)
