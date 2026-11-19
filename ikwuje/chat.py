"""Data models: a Message and a Chat that holds many messages."""

import uuid
from datetime import datetime


def _now():
    return datetime.now().isoformat(timespec="seconds")


class Message:
    """One message in a chat. role is 'user' or 'assistant'."""

    def __init__(self, role, content, timestamp=None):
        self.role = role
        self.content = content
        self.timestamp = timestamp or _now()

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["role"], data["content"], data.get("timestamp"))


class Chat:
    """A conversation: an id, a title and a list of Message objects."""

    DEFAULT_TITLE = "New chat"

    def __init__(self, title=DEFAULT_TITLE, chat_id=None, messages=None, created_at=None):
        self.id = chat_id or uuid.uuid4().hex[:8]
        self.title = title
        self.messages = messages if messages is not None else []
        self.created_at = created_at or _now()

    def add_message(self, role, content):
        message = Message(role, content)
        self.messages.append(message)
        # The first thing the user says becomes the chat title.
        if self.title == self.DEFAULT_TITLE and role == "user":
            self.title = content[:30]
        return message

    def to_api_messages(self):
        """The simple format AI APIs expect: [{'role': ..., 'content': ...}]."""
        return [{"role": m.role, "content": m.content} for m in self.messages]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at,
            "messages": [m.to_dict() for m in self.messages],
        }

    @classmethod
    def from_dict(cls, data):
        messages = [Message.from_dict(m) for m in data.get("messages", [])]
        return cls(
            title=data.get("title", cls.DEFAULT_TITLE),
            chat_id=data["id"],
            messages=messages,
            created_at=data.get("created_at"),
        )
