import os
import dotenv
import telegram
import random

dotenv.load_dotenv('.env')
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

bot = telegram.Bot(token=TG_BOT_TOKEN)

chat_id = "-1002313823580"

photo_list = os.listdir('photos')

random_photo = os.path.join('photos', random.choice(photo_list))

bot.send_photo(chat_id=chat_id, photo=open(random_photo, "rb"))