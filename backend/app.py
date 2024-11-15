import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import openai
import speech_recognition as sr


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

AZURE_SPEECH_KEY = "DNUb3KJSrfai4w3UMoJ5MGSFBnOVhNKPiFH5s04VxGMBwqHb700ZJQQJ99AKACYeBjFXJ3w3AAAYACOGr9sF"
AZURE_REGION= "eastus"

# Initialize the recognizer
recognizer = sr.Recognizer()

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


@app.route("/speech-to-text", methods=["POST"])
@cross_origin()  # Explicitly add CORS to this route as well
def speech_to_text():
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        audio_file = request.files['audio']


        # Use SpeechRecognition to recognize speech from the audio file
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            print(audio_data)
            text = recognizer.recognize_google(audio_data)  # Using Google Web Speech API

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)



# @app.route("/text-to-speech", methods=["POST"])
# def text_to_speech():
#     data = request.get_json()
#     if not data or "text" not in data:
#         return jsonify({"error": "Text input is required"}), 400

#     text = data["text"]

#     # Initialize the speech synthesis configuration
#     speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
#     synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

#     # Synthesize speech
#     result = synthesizer.speak_text_async(text).get()

#     if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#         return jsonify({"message": "Speech synthesized successfully"})
#     else:
#         return jsonify({"error": "Speech synthesis failed"}), 500

