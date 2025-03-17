import logging
from telegram.ext import Application, MessageHandler, filters
from config import TOKEN
from handlers import forward_message, handle_migration, error_handler

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Запускает бота в режиме polling"""
    app = Application.builder().token(TOKEN).build()

    # Добавляем обработчики для всех типов сообщений
    app.add_handler(MessageHandler(filters.ALL, forward_message))

    # Обработчик миграции чатов
    app.add_handler(MessageHandler(filters.StatusUpdate.MIGRATE, handle_migration))

    # Обработчик ошибок
    app.add_error_handler(error_handler)

    logger.info("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()