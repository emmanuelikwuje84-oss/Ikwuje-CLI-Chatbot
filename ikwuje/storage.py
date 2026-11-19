"""Saving and loading chats as JSON files in the data/ folder."""

import json
from pathlib import Path

from ikwuje.chat import Chat

DATA_DIR = Path("data")


def _chat_path(chat_id, data_dir):
    return Path(data_dir) / f"{chat_id}.json"


def save_chat(chat, data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    with open(_chat_path(chat.id, data_dir), "w", encoding="utf-8") as file:
        json.dump(chat.to_dict(), file, indent=2, ensure_ascii=False)


def load_chat(chat_id, data_dir=DATA_DIR):
    """Return a Chat, or None if the file is missing or damaged."""
    try:
        with open(_chat_path(chat_id, data_dir), encoding="utf-8") as file:
            data = json.load(file)
        return Chat.from_dict(data)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None


def list_chats(data_dir=DATA_DIR):
    """All saved chats, newest first. Damaged files are skipped."""
    chats = []
    for path in Path(data_dir).glob("*.json"):
        chat = load_chat(path.stem, data_dir)
        if chat is not None:
            chats.append(chat)
    chats.sort(key=lambda chat: chat.created_at, reverse=True)
    return chats


def delete_chat(chat_id, data_dir=DATA_DIR):
    """Delete a chat file. Returns True if something was deleted."""
    path = _chat_path(chat_id, data_dir)
    if path.exists():
        path.unlink()
        return True
    return False
