from telegram import Bot
from telegram.error import TelegramError


async def send_alert(
    bot_token: str,
    chat_id: str,
    message: str,
) -> None:
    """
    Sends a message to a Telegram chat.

    :param bot_token: Your Telegram bot token
    :param chat_id: ID of the chat (or channel) to send the message to
    :param message: The message text
    :return: None
    """
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="HTML",
        )
    except TelegramError as e:
        print(f"Error sending message to Telegram: {e}")
