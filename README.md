# Real time chat

A real-time chat application built with React and typescript (frontend) and Python with Flask (backend). The project supports real-time messaging using text and attempts to use voice input as well.

At the moment, the app runs locally because it uses a .env file. Sample .env file is attached to the code. In order to make it run on cloud e.g. via lambda or azure function app, the secrets from .env file need to be stored in application settings, or provided via variables in the CD pipeline to be used during runtime.


## How to run locally

```
git clone https://github.com/rupshabagchi/chat.git
cd chat
make install-backend
make start-backend

// in another terminal instance to run frontend.
make run-frontend
```

