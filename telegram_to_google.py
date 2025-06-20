import os
import json
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GOOGLE_CREDENTIALS = os.environ.get('GOOGLE_CREDENTIALS')

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

if GOOGLE_CREDENTIALS:
    creds_dict = json.loads(GOOGLE_CREDENTIALS)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
else:
    creds = ServiceAccountCredentials.from_json_keyfile_name("telegram-bot-credentials.json", scope)

client = gspread.authorize(creds)
sheet = client.open("TelegramData").sheet1

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    username = message.from_user.username or ""
    text = message.text
    sheet.append_row([username, text])
    bot.reply_to(message, "✅ Записано в таблицу")

print("Бот запущен и ожидает сообщения...")
bot.polling()