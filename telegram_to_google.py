import os
import json
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Загрузка токена и учетных данных из переменных окружения
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS")

# Области доступа к Google Sheets и Google Drive
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Настройка авторизации через gspread
if GOOGLE_CREDENTIALS:
    creds_dict = json.loads(GOOGLE_CREDENTIALS)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
else:
    creds = ServiceAccountCredentials.from_json_keyfile_name("telegram-bot-credentials.json", scope)

client = gspread.authorize(creds)
sheet = client.open("ТС-Энерго Бот").worksheet("Лист6")

# Настройка телеграм-бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши мне что-нибудь, и я сохраню это в таблицу Google Sheets.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user = message.from_user.first_name
    text = message.text
    sheet.append_row([user, text])
    bot.reply_to(message, "Сохранил в таблицу!")

print("Бот запущен и ожидает сообщения...")
bot.polling()
