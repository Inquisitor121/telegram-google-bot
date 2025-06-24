import os
import json
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Загрузка токена телеграм-бота из переменной окружения
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Пути и области доступа для Google Sheets
CREDENTIALS_PATH = "/etc/secrets/credentials.json"
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Загрузка учетных данных
with open(CREDENTIALS_PATH) as f:
    creds_dict = json.load(f)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPES)

# Авторизация и подключение к Google Таблице
client = gspread.authorize(creds)
sheet = client.open("ТС-Энерго Бот").worksheet("Лист6")  # Заменить, если названия другие

# Настройка Telegram-бота
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
