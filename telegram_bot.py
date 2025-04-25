import os
import dotenv
import telegram
import random
import argparse
import time
from main import folder

if __name__ == '__main__':
    dotenv.load_dotenv('.env')
    TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
    TG_CHAT_ID = os.environ["TG_CHAT_ID"]

    bot = telegram.Bot(token=TG_BOT_TOKEN)
    chat_id = TG_CHAT_ID

    photo_list = os.listdir(folder)

    parser = argparse.ArgumentParser() 
    parser.add_argument('--delay', type=int, default=14400, help='Задрежка отправки сообщений')
    args = parser.parse_args()

    max_retries = 5
    retry_delay = 5

    while True:
        random_photo = os.path.join(folder, random.choice(photo_list))
        for attemp in range(max_retries):
            try:
                with open(random_photo, "rb") as file:
                    bot.send_photo(chat_id=chat_id, photo=file)
                break
            except telegram.error.NetworkError as e:
                print(f'Ошибка соединения (попытка {attemp + 1}/{max_retries}): {e}')
                if attemp < max_retries -1:
                    print(f'Повторная попытка через {retry_delay} секунд...')
                    time.sleep(retry_delay)
                    retry_delay *= 2
                continue
            except Exception or telegram.error as e:
                print(f'Непредвиденная ошибка: {e}')
                break

        time.sleep(args.delay)
        random.shuffle(photo_list)
        retry_delay = 5