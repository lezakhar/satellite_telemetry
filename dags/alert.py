from telegram import Bot
from telegram.error import TelegramError


async def send_alert(
    bot_token: str,
    chat_id: str,
    message: str,
) -> None:
    """
    Отправляет сообщение в Telegram чат.

    :param bot_token: Токен вашего Telegram бота
    :param chat_id: ID чата (или канала) для отправки сообщения
    :param message: Текст сообщения
    :return: True если отправка успешна, False в случае ошибки
    """
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(
            chat_id=chat_id,
            text=message,
        )
    except TelegramError as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")
