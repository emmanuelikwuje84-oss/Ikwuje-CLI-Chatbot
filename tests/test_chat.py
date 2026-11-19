from ikwuje.chat import Chat, Message


def test_first_user_message_becomes_title():
    chat = Chat()
    chat.add_message("user", "What is Python?")
    assert chat.title == "What is Python?"


def test_title_not_changed_by_later_messages():
    chat = Chat()
    chat.add_message("user", "First")
    chat.add_message("assistant", "Hi")
    chat.add_message("user", "Second")
    assert chat.title == "First"


def test_to_api_messages_format():
    chat = Chat()
    chat.add_message("user", "Hello")
    chat.add_message("assistant", "Hi there")
    assert chat.to_api_messages() == [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    ]


def test_chat_survives_dict_round_trip():
    chat = Chat()
    chat.add_message("user", "Hello")
    restored = Chat.from_dict(chat.to_dict())
    assert restored.id == chat.id
    assert restored.title == chat.title
    assert restored.messages[0].content == "Hello"


def test_message_round_trip():
    message = Message("user", "Hey")
    assert Message.from_dict(message.to_dict()).content == "Hey"
