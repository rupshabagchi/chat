# Real time chat

A real-time chat application built with React and typescript (frontend) and Python with Flask (backend). The project supports real-time messaging using text and attempts to use voice input as well.

At the moment, the app runs locally because it uses a .env file. Sample .env file is attached to the code. In order to make it run on cloud e.g. via lambda or azure function app, the secrets from .env file need to be stored in application settings, or provided via variables in the CD pipeline to be used during runtime.

There are 3 apis here:
* chat api: Basic socket based chat with predetermined answers
* open-ai integrated chat: Uses azure openai api to complete chats
* speech to text api: Takes input audio and transcribes it. Intention was to use the transcribed text as part of input to openai api (as azure speech recognition api appears to be less accurate to me and relatively more expensive)


## How to run locally

```
git clone https://github.com/rupshabagchi/chat.git
cd chat
make install-backend
make start-backend

// in another terminal instance to run frontend.
make run-frontend
```

