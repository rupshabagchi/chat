from flask import Flask, request, jsonify
import azure.cognitiveservices.speech as speechsdk
import os

AZURE_API_KEY = 'DNUb3KJSrfai4w3UMoJ5MGSFBnOVhNKPiFH5s04VxGMBwqHb700ZJQQJ99AKACYeBjFXJ3w3AAAYACOGr9sF'
AZURE_REGION = 'eastus'

def text_to_speech(text):
    """Convert text to speech using Azure's TTS API."""
    # Set up the speech configuration
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # Create the synthesizer with the given text and audio config
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Start synthesizing
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Successfully synthesized the text: {text}")
    else:
        print(f"Speech synthesis failed: {result.error_details}")
        return None

    return "Successfully synthesized speech."


def speech_to_text(audio_file):
    """Convert speech from an audio file to text using Azure's Speech-to-Text API."""
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
    audio_input = speechsdk.audio.AudioConfig(filename=audio_file)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized speech: {result.text}")
        return result.text
    else:
        print(f"Speech recognition failed: {result.error_details}")
        return None
