import os
import dotenv
import telegram
import random
import argparse
import time

dotenv.load_dotenv('.env')
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

bot = telegram.Bot(token=TG_BOT_TOKEN)

chat_id = TG_CHAT_ID

photo_list = os.listdir('photos')

parser = argparse.ArgumentParser() 
parser.add_argument('--delay', type=int)
args = parser.parse_args()

delay = args.delay if args.delay else 14400

while True:
    random_photo = os.path.join('photos', random.choice(photo_list))
    bot.send_photo(chat_id=chat_id, photo=open(random_photo, "rb"))
    time.sleep(delay)
    random.shuffle(photo_list)