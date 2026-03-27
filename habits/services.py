import requests
from django.conf import settings


def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    params = {
        "chat_id": chat_id,
        "text": text,
    }

    response = requests.post(url, params=params)

    if response.status_code != 200:
        raise Exception(
            f"Ошибка отправки сообщения в Telegram: "
            f"{response.status_code} - {response.text}"
        )

    return response.json()
