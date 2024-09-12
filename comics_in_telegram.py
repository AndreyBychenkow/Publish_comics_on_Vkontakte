import os
import random

import requests
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError


def get_random_xkcd():
    comic_response = requests.get('https://xkcd.com/info.0.json')
    comic_response.raise_for_status()
    comic_data = comic_response.json()

    random_comic_number = random.randint(1, comic_data['num'])
    random_comic_response = requests.get(
        f'https://xkcd.com/{random_comic_number}/info.0.json')
    random_comic_response.raise_for_status()
    random_comic_data = random_comic_response.json()

    return random_comic_data['img'], random_comic_data['title']


def post_comic_to_telegram(bot, chat_id, image_url, title):
    image_response = requests.get(image_url)
    image_response.raise_for_status()

    file_path = 'comic.png'
    with open(file_path, 'wb') as file:
        file.write(image_response.content)

    with open(file_path, 'rb') as file:
        bot.send_photo(chat_id=chat_id, photo=file, caption=title)

    os.remove(file_path)


def main():
    load_dotenv()

    telegram_bot_token = os.getenv('TELEGRAM_ACCESS_TOKEN')
    telegram_group_id = os.getenv('TELEGRAM_CLIENT_ID')

    bot = Bot(token=telegram_bot_token)

    try:

        image_url, title = get_random_xkcd()
        post_comic_to_telegram(bot, telegram_group_id, image_url, title)
    except requests.exceptions.RequestException as e:
        print(f'Ошибка сети: {e}')
    except TelegramError as e:
        print(f'Ошибка Telegram API: {e}')


if __name__ == "__main__":
    main()
