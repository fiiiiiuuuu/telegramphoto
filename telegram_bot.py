import os
import dotenv
import telegram
import random
import argparse
import time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fld', default='photos', help='название папки (необязательно)')
    parser.add_argument('--delay', type=int, default=14400, help='Задержка отправки сообщений')
    return parser.parse_args()


def send_photo(bot, chat_id, photos, fld_name, retry_delay, max_retries=5):
        random_photo = os.path.join(fld_name, random.choice(photos))
        for attempt in range(max_retries):
                try:
                    with open(random_photo, "rb") as file:
                        bot.send_photo(chat_id=chat_id, photo=file)
                    return True
                except telegram.error.NetworkError as e:
                    print(f'Ошибка соединения (попытка {attempt + 1}/{max_retries}): {e}')
                    if attempt < max_retries - 1:
                        print(f'Повторная попытка через {retry_delay} секунд...')
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    continue
                except Exception as e:
                    print(f'Непредвиденная ошибка: {e}')
                    break
        return False
        


def main():
    dotenv.load_dotenv('.env')
    tg_bot_token = os.environ["TG_BOT_TOKEN"]
    tg_chat_id = os.environ["TG_CHAT_ID"]
    bot = telegram.Bot(token=tg_bot_token)
    chat_id = tg_chat_id 
    fld_name = parse_args().fld
    delay = parse_args().delay

    photos = os.listdir(fld_name)

    while True:
        send_photo(bot, chat_id, photos, fld_name, retry_delay=5)
        time.sleep(delay)
        random.shuffle(photos)


if __name__ == '__main__':
    main()