from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from transformers import pipeline, Conversation

app = Flask(__name__)
CORS(app, support_credentials=True)
cors = CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_HEADERS'] = 'application/json'

chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium", pad_token_id=50256)

@app.route('/chat', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def chat():
    request.headers['Access-Control-Allow-Origin']='*'
    request.headers['Access-Control-Allow-Methods']='GET, POST, PUT, OPTIONS'
    request.headers["Access-Control-Allow-Headers"]="Access-Control-Request-Headers,Access-Control-Allow-Methods,Access-Control-Allow-Headers,Access-Control-Allow-Origin, Origin, X-Requested-With, Content-Type, Accept"
    if request.method == 'OPTIONS': 
        return build_preflight_response()
    user_input = request.json.get("message")
    conversation = Conversation(user_input)
    response = chatbot(conversation)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return build_actual_response(jsonify({"response": response.generated_responses[0]}))

def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True)
