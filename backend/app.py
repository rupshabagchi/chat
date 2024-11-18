import os
import io
import openai
import speech_recognition as sr
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pydub import AudioSegment
from utils.strip import strip_response
from flask_socketio import SocketIO, emit
from utils.chatbot_rules import get_bot_response

# Load environment variables from the .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for WebSocket connections

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


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if user_message:
        bot_response = get_bot_response(user_message)
        return jsonify({"response": bot_response}), 200
    else:
        return jsonify({"error": "No message provided"}), 400


@socketio.on('send_message')
def handle_message(msg):
    print(f"Received message: {msg}")

    bot_response = get_bot_response(msg)
    emit('receive_message', {'message': bot_response}, broadcast=True)


@app.route("/chat-openai", methods=["POST"])
def chat_openai():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    start_phrase = f"""
    <|im_start|>system\n
    Imagine you are a chatbot. 
    Your job is to chat with me casually. 
    If I say 'hello,' just reply with a greeting as if we're having a normal conversation. 
    No code in any programming language, just plain text. No prose.
    Follow these examples to guide your answer.
    Example 1:
    User: "Hello, how are you?"
    You: "I'm doing well, thank you! How can I assist you today?"

    Example 2:
    User: "What is the capital of France?"
    You: "The capital of France is Paris."

    Example 3:
    User: "Can you tell me a joke?"
    You: "Sure! Why don't scientists trust atoms? Because they make up everything!"

    Now, given the input below, respond appropriately:\n<|im_end|>\n
    <|im_start|>user\n "{user_message}"\n<|im_end|>\n<|im_start|>chatbot\n
    """

    try:
        _response = openai.Completion.create(
           engine=deployment_name, 
           prompt=start_phrase, 
           max_tokens=150, 
           temperature=0.7,
           top_p=0.5,
           stop=["<|im_end|>"]
        )
        print(_response.choices[0])
        response = strip_response(_response.choices[0].text)

        # if response['choices'][0]['finish_reason'] == 'length':
        #     return jsonify({"error": "The response was cut off due to token limit."}), 429

        return jsonify({"response": response})

    except Exception as e:
        if "RateLimitError" in str(e):
            return jsonify({"response": "rate limit error"}), 429
        return jsonify({"response": "error:"+str(e)}), 500


def preprocess_audio(audio_file):
    print("audio file", audio_file)
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(16000).set_channels(1)
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

        recognizer = sr.Recognizer()

        processed_audio = preprocess_audio(audio_file)

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
#     speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
#     synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
#     result = synthesizer.speak_text_async(text).get()
#     if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#         return jsonify({"message": "Speech synthesized successfully"})
#     else:
#         return jsonify({"error": "Speech synthesis failed"}), 500

