"""Ikwuje: a terminal AI chatbot that saves your chats."""

from ikwuje import storage
from ikwuje.ai import AIError, get_reply
from ikwuje.chat import Chat


def show_chats(chats):
    for number, chat in enumerate(chats, start=1):
        print(f"{number}. {chat.title}  ({len(chat.messages)} messages, {chat.created_at})")


def choose_chat(action):
    """Show saved chats and let the user pick one by number."""
    chats = storage.list_chats()
    if not chats:
        print("No saved chats yet.")
        return None

    show_chats(chats)
    choice = input(f"Number of the chat to {action} (Enter to cancel): ").strip()
    if not choice:
        return None
    try:
        index = int(choice) - 1
    except ValueError:
        print("Please enter a number.")
        return None
    if 0 <= index < len(chats):
        return chats[index]
    print("That number is not in the list.")
    return None


def chat_session(chat):
    print(f"\n--- {chat.title} --- (type /back to return to the menu)")
    for message in chat.messages:
        name = "You" if message.role == "user" else "Ikwuje"
        print(f"{name}: {message.content}")

    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not text:
            continue
        if text.lower() == "/back":
            break

        chat.add_message("user", text)
        try:
            reply = get_reply(chat.to_api_messages())
        except AIError as error:
            chat.messages.pop()  # remove the unanswered message
            print(f"[Error] {error}")
            continue

        chat.add_message("assistant", reply)
        print(f"Ikwuje: {reply}\n")
        storage.save_chat(chat)


def delete_flow():
    chat = choose_chat("delete")
    if chat is None:
        return
    confirm = input(f"Delete '{chat.title}'? (y/n): ").strip().lower()
    if confirm == "y":
        storage.delete_chat(chat.id)
        print("Deleted.")
    else:
        print("Cancelled.")


def main():
    print("Welcome to Ikwuje!")
    while True:
        print("\n1. New chat\n2. Open a chat\n3. Delete a chat\n4. Quit")
        choice = input("Choose: ").strip()

        if choice == "1":
            chat_session(Chat())
        elif choice == "2":
            chat = choose_chat("open")
            if chat is not None:
                chat_session(chat)
        elif choice == "3":
            delete_flow()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please choose 1, 2, 3 or 4.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
