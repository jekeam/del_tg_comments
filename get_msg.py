import asyncio

from pyrogram import Client

from config import API_ID, API_HASH


CHAT_ID = -1001710930210
MESSAGE_ID = 6618

proxy_settings = {
    "scheme": "socks5",       # или "http"
    "hostname": "127.0.0.1",  # адрес прокси
    "port": 1080
}


async def main():
    async with Client(
        "deleter",
        API_ID,
        API_HASH,
        proxy=proxy_settings
    ) as app:
        msg = await app.get_messages(CHAT_ID, MESSAGE_ID)

        if not msg:
            print("Сообщение не найдено")
            return

        print("ID:", msg.id)
        print("Дата:", msg.date)

        if msg.from_user:
            print("Автор:", msg.from_user.first_name, msg.from_user.last_name or "")
            print("Username:", f"@{msg.from_user.username}" if msg.from_user.username else "нет")
            print("User ID:", msg.from_user.id)

        print("Текст:")
        print(msg.text or msg.caption or "[текста нет]")


if __name__ == "__main__":
    asyncio.run(main())