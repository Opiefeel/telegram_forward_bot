import logging
from telegram import Update
from telegram.ext import CallbackContext

from config import TARGET_CHAT_ID

logger = logging.getLogger(__name__)


async def forward_message(update: Update, context: CallbackContext):
    """Пересылает сообщение в целевой чат, если оно от другого источника"""
    if update.effective_chat.id == TARGET_CHAT_ID:
        return

    # Проверяем, есть ли сообщение
    if not update.message:
        return

    try:
        await context.bot.forward_message(
            chat_id=TARGET_CHAT_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id,
        )
        logger.info(f"Сообщение {update.message.message_id} переслано в {TARGET_CHAT_ID}")

    except Exception as e:
        logger.error(f"Ошибка при пересылке: {e}")


async def handle_migration(update: Update, context: CallbackContext):
    """Обрабатывает миграцию группы в супергруппу"""
    if update.message.migrate_to_chat_id:
        new_chat_id = update.message.migrate_to_chat_id
        logger.info(f"Группа мигрировала в супергруппу. Новый chat_id: {new_chat_id}")


async def error_handler(update: object, context: CallbackContext):
    """Логирует ошибки, чтобы бот не падал"""
    logger.error(f"Ошибка: {context.error}")