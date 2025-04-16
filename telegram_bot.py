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

    while True:
        random_photo = os.path.join(folder, random.choice(photo_list))
        with open(random_photo, "rb") as file:
            bot.send_photo(chat_id=chat_id, photo=file)
        time.sleep(args.delay)
        random.shuffle(photo_list)