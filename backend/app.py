from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline, Conversation

app = Flask(__name__)
CORS(app)  # Ajoute cette ligne pour activer CORS

chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium", pad_token_id=50256)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    conversation = Conversation(user_input)  # Crée un objet Conversation
    response = chatbot(conversation)
    return jsonify({"response": response.generated_responses[0]})  # Utilise generated_responses

if __name__ == '__main__':
    app.run(debug=True)
