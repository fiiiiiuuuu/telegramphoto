import os
import dotenv
import telegram

dotenv.load_dotenv('.env')
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

bot = telegram.Bot(token=TG_BOT_TOKEN)
