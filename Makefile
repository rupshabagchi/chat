PROJECT = chat
ifndef VERSION
VERSION := $(shell git describe --tags --always)
endif

.PHONY: install-backend
install-backend:
	pip install -r requirements.txt

.PHONY: install-frontend
install-frontend:
	cd frontend && npm install

.PHONY: start-backend
start-backend:
	cd backend && \
	echo "Starting Flask backend server..." && \
	python app.py

.PHONY: lint-backend
start-backend:
	cd backend && \
	python -m flake8 backend/
