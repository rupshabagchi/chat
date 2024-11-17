import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from pydub import AudioSegment
import io
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


def preprocess_audio(audio_file):
    print("audio file", audio_file)
    audio = AudioSegment.from_file(audio_file)  # Load the audio
    audio = audio.set_frame_rate(16000).set_channels(1)  # Standardize frame rate and channels
    processed_audio = io.BytesIO()
    audio.export(processed_audio, format="wav")  # Export as WAV
    processed_audio.seek(0)
    return processed_audio

@app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        audio_file = request.files['audio']

        # Initialize the recognizer
        recognizer = sr.Recognizer()

        processed_audio = preprocess_audio(audio_file)
        # Use SpeechRecognition to recognize speech from the audio file
        with sr.AudioFile(processed_audio) as source:
            audio_data = recognizer.record(source)
            print("comes here as well", audio_data)
            text = recognizer.recognize_google(audio_data)  # Using Google Web Speech API
            print("Recognized speech ", text)

        return jsonify({"text": text})

    except sr.WaitTimeoutError:
        return jsonify({"error": "Speech recognition timed out"}), 504
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Google Speech API request failed: {e}"}), 500


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

