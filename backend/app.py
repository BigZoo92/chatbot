import os
import tensorflow as tf

# Limiter l'utilisation de la mémoire par TensorFlow
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if physical_devices:
    for device in physical_devices:
        tf.config.experimental.set_memory_growth(device, True)

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from transformers import pipeline, Conversation, TFAutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_HEADERS'] = 'application/json'

# Utilisation de TensorFlow comme backend
model_name = "sshleifer/tiny-gpt2"
model = TFAutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
chatbot = pipeline("conversational", model=model, tokenizer=tokenizer)

@app.route('/')
def index():
    return jsonify({"message": "Hello, world! Your Flask app is running."})

@app.route('/chat', methods=['POST', 'OPTIONS'])
@cross_origin()
def chat():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "No message provided"})

    conversation = Conversation(user_input)
    response = chatbot(conversation)
    generated_response = response.generated_responses[0].text if response.generated_responses else "No response generated"
    return jsonify({"response": generated_response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
