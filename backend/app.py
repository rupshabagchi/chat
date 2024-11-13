import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from utils.voiceOperations import text_to_speech

# Load environment variables from the .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Enable CORS for all origins
CORS(app, resources={r'/*' : {'origins': ['http://localhost:5173']}})
app.config['CORS_HEADERS'] = 'Content-Type'


# Set up OpenAI API key and endpoint (get from Azure Portal)
openai.api_key = os.getenv("api_key")
openai.api_base = os.getenv("api_base")
openai.api_type = os.getenv("api_type")
openai.api_version = os.getenv("api_version")
deployment_name=os.getenv("deployment_name")

@app.route("/")
def not_found():
    return "error: route not found", 404


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    # start_phrase = 'Respond in a pirate accent.'

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Send user input to OpenAI via Azure API
        # response = openai.Completion.create(
        #    engine=deployment_name, prompt=start_phrase, max_tokens=10
        # )

        # Extract the response text from OpenAI
        # answer = response.choices[0].text.strip()

        return jsonify({"response": "hello"})

    except Exception as e:
        return jsonify({"error": e}), 500


@app.route('/api/speech-to-speech', methods=['POST'])
def speech_to_speech():
    """Receive transcribed text from the frontend, convert it to speech, and return the audio URL."""
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    audio_url = text_to_speech(text)

    return jsonify({'audioUrl': audio_url})



if __name__ == "__main__":
    app.run(debug=True, port=5000)
