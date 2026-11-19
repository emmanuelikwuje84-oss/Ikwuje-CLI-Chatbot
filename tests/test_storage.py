from ikwuje import storage
from ikwuje.chat import Chat


def make_chat(text="Hello"):
    chat = Chat()
    chat.add_message("user", text)
    return chat


def test_save_and_load(tmp_path):
    chat = make_chat()
    storage.save_chat(chat, tmp_path)
    loaded = storage.load_chat(chat.id, tmp_path)
    assert loaded.title == chat.title
    assert loaded.messages[0].content == "Hello"


def test_load_missing_returns_none(tmp_path):
    assert storage.load_chat("nope", tmp_path) is None


def test_damaged_file_is_skipped(tmp_path):
    (tmp_path / "broken.json").write_text("{ not valid json")
    good = make_chat()
    storage.save_chat(good, tmp_path)
    chats = storage.list_chats(tmp_path)
    assert [c.id for c in chats] == [good.id]


def test_list_on_missing_folder(tmp_path):
    assert storage.list_chats(tmp_path / "does-not-exist") == []


def test_delete(tmp_path):
    chat = make_chat()
    storage.save_chat(chat, tmp_path)
    assert storage.delete_chat(chat.id, tmp_path) is True
    assert storage.delete_chat(chat.id, tmp_path) is False
