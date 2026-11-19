# Ikwuje-CLI-Chatbot

A terminal AI chatbot that saves every conversation. Project 1 of my AI Engineering roadmap.

## Features
- Start new chats, reopen old ones, delete chats
- Chats saved as JSON files in `data/`
- Friendly error messages (no internet, rate limit, bad key)
- Unit tests with pytest

## Setup
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then put your Gemini key in .env
```

Get a free key from Google AI Studio.

## Run
```bash
python main.py
```

## Test
```bash
pytest
```

## Structure
- `main.py` - menu and chat loop
- `ikwuje/chat.py` - Message and Chat classes
- `ikwuje/storage.py` - save/load JSON
- `ikwuje/ai.py` - calls the AI API
- `tests/` - pytest tests
