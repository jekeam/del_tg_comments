import asyncio

from pyrogram import Client

from config import API_ID, API_HASH


CHAT_ID = -1001710930210
MY_MESSAGE_ID = 9121

proxy_settings = {
    "scheme": "socks5",
    "hostname": "127.0.0.1",
    "port": 1080
}


def get_author(msg):
    if msg.from_user:
        username = f"@{msg.from_user.username}" if msg.from_user.username else ""
        name = " ".join(
            x for x in [
                msg.from_user.first_name,
                msg.from_user.last_name
            ] if x
        )
        return f"{name} {username}".strip() or str(msg.from_user.id)

    if msg.sender_chat:
        username = f"@{msg.sender_chat.username}" if msg.sender_chat.username else ""
        return f"{msg.sender_chat.title} {username}".strip()

    return "unknown"


def get_text(msg):
    return msg.text or msg.caption or "[нет текста]"


async def main():
    async with Client(
        "deleter",
        API_ID,
        API_HASH,
        proxy=proxy_settings
    ) as app:
        my_msg = await app.get_messages(CHAT_ID, MY_MESSAGE_ID)

        if not my_msg:
            print("Твоё сообщение не найдено")
            return

        if not my_msg.reply_to_message_id:
            print("Это сообщение не было ответом")
            return

        replied_msg = await app.get_messages(CHAT_ID, my_msg.reply_to_message_id)

        if not replied_msg:
            print(f"Исходное сообщение {my_msg.reply_to_message_id} не найдено")
            return

        print(f"chat_id: {CHAT_ID}")
        print(f"my_message_id: {my_msg.id}")
        print(f"reply_to_message_id: {my_msg.reply_to_message_id}")
        print()
        print(f"original_message_id: {replied_msg.id}")
        print(f"date: {replied_msg.date}")
        print(f"author: {get_author(replied_msg)}")
        print(f"text: {get_text(replied_msg)}")


if __name__ == "__main__":
    asyncio.run(main())