import asyncio
import logging
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.errors import (
    FloodWaitError,
    ChatAdminRequiredError,
    ChannelPrivateError,
    UserNotParticipantError,
    MessageIdInvalidError,
    MessageNotModifiedError,
    ChatIdInvalidError
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

# Конфигурация бота
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")

if not all([API_ID, API_HASH, BOT_TOKEN, TARGET_CHAT_ID]):
    raise EnvironmentError("Не все переменные окружения заданы правильно.")

try:
    TARGET_CHAT_ID = int(TARGET_CHAT_ID)
except ValueError:
    raise ValueError("TARGET_CHAT_ID должен быть целым числом.")

# Инициализация клиента
client = TelegramClient('bot_session', API_ID, API_HASH)


@client.on(events.NewMessage)
async def new_message_handler(event):

    source_chat_id = event.chat_id

    if source_chat_id == TARGET_CHAT_ID:
        logger.info("Сообщение из целевого чата, не пересылаем.")
        return

    logger.info(f"Новое сообщение от {source_chat_id}: {event.raw_text}")
    try:
        await client.send_message(TARGET_CHAT_ID, f"{event.raw_text}")
    except Exception as e:
        logger.error(f"Ошибка при пересылке сообщения: {type(e).__name__}: {e}")


async def main():
    try:
        logger.info(f"Запуск бота с TARGET_CHAT_ID: {TARGET_CHAT_ID}")
        await client.start(bot_token=BOT_TOKEN)
        logger.info("Бот запущен и готов к работе")

        try:
            await client.send_message(
                TARGET_CHAT_ID,
                "Тестовое сообщение для проверки работы бота ✅ #2")
            logger.info("Тестовое сообщение успешно отправлено")
        except ChatIdInvalidError as e:
            logger.error(f"Недействительный ID чата: {e}")
        except Exception as e:
            logger.error(
                f"Ошибка при отправке тестового сообщения: {type(e).__name__}: {e}")

        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"Критическая ошибка: {type(e).__name__}: {e}")
    finally:
        try:
            await client.send_message(TARGET_CHAT_ID, "⚠️ Бот останавливается")
        except:
            pass


if __name__ == "__main__":
    asyncio.run(main())
