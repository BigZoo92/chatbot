from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline, Conversation

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "https://chatbot-d5g63wsrv-bigzoos-projects.vercel.app"}})

chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium", pad_token_id=50256)

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    request.headers['Access-Control-Allow-Origin']='*'
    request.headers['Access-Control-Allow-Methods']='GET, POST, PUT, OPTIONS'
    request.headers["Access-Control-Allow-Headers"]="Access-Control-Request-Headers,Access-Control-Allow-Methods,Access-Control-Allow-Headers,Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept"
    if request.method == 'OPTIONS':
        return jsonify({}), 200 
    user_input = request.json.get("message")
    conversation = Conversation(user_input)
    response = chatbot(conversation)
    return jsonify({"response": response.generated_responses[0]})

if __name__ == '__main__':
    app.run(debug=True)
