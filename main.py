import asyncio
import time
import traceback
from time import sleep

from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait, NotAcceptable

from config import API_ID, API_HASH, CHAT_ID_EXCLUDE, TIME_SLEEP_SEC
from log import app_log

DIALOGS = []


async def delete_all_messages():
    async with Client("deleter", API_ID, API_HASH) as app:
        app_log.info("Подключение к Telegram...")

        me = await app.get_me()
        my_id = me.id

        async for dialog in app.get_dialogs():
            if dialog.chat.id not in DIALOGS:
                sleep(1)
                chat = await app.get_chat(dialog.chat.id)

                if chat.linked_chat:
                    DIALOGS.append(chat.linked_chat.id)
                    app_log.info(f"add link: {chat.linked_chat.id}")
                if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                    DIALOGS.append(chat.id)
                    app_log.info(f"add chat: {chat.id}")

        for chat_id in DIALOGS:
            try:
                sleep(1)
                chat = await app.get_chat(chat_id)

                if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
                    continue

                if chat_id > 0 or chat_id in CHAT_ID_EXCLUDE:
                    continue

                if chat.is_creator:
                    # app_log.info(f"Пропускаем свой чат: {chat.title or chat.id}")
                    continue

                cnt = await app.search_messages_count(chat.id, from_user=my_id)

                if cnt == 0:
                    continue

                app_log.info(
                    f"ИД: {chat.id}\n"
                    f"{'@' + chat.username if chat.username else ''}: {chat.title or chat.first_name or ''} {chat.last_name or ''}"
                    f"\nУдалить сообщений: {cnt}\n"
                )

                async for msg in app.search_messages(chat.id, from_user=my_id):
                    try:
                        if msg.service:
                            app_log.info(f"Сервисное сообщение пропущено {chat.id}: {msg.id}")
                            continue

                        # app_log.info(f"Удалено сообщение в чате {chat.id}: {msg.text or msg.caption}")
                        await app.delete_messages(chat.id, msg.id)
                        app_log.info(f"Удалено сообщение в чате {chat.id}: {msg}")
                    except Exception as e:
                        app_log.error(f"Ошибка при удалении сообщения {msg.id} в {chat.title}: {e}")

            except FloodWait as flood_wait:
                app_log.error(f"FloodWait! Спим {flood_wait.value} секунд...")
                sleep(flood_wait.value)

            except NotAcceptable:
                app_log.error(f"NotAcceptable! Удалям ид из списка обхода: {chat_id}")
                DIALOGS.pop(DIALOGS.index(chat_id))

            except Exception as e:
                app_log.error(f"Ошибка при обработке чата {chat_id}: {e}, {traceback.format_exc()}")

        app_log.info("Удаление завершено!")


if __name__ == "__main__":
    while True:
        asyncio.run(delete_all_messages())
        app_log.info(f"I sleep hours: {TIME_SLEEP_SEC / 60 / 60}")
        time.sleep(TIME_SLEEP_SEC)
