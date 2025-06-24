import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json

# Токен Telegram из переменной окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Путь к JSON-файлу с ключом
creds_path = "telegram-bot-credentials.json"
with open(creds_path) as source:
    creds_dict = json.load(source)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Открытие Google Таблицы
spreadsheet = client.open("ТС-Энерго Бот")
sheet = spreadsheet.worksheet("Лист6")

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        parts = message.text.split("/")
        if len(parts) != 5:
            bot.reply_to(message, "Пожалуйста, введите данные в формате:\nСумма/Статья/Контрагент/Комментарий/Объект")
            return

        date = datetime.now().strftime("%Y-%m-%d")
        username = message.from_user.first_name
        row = [date, username] + parts

        sheet.append_row(row)
        bot.reply_to(message, "✅ Данные добавлены в таблицу.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка при добавлении данных: {e}")

# Запуск бота
bot.polling(none_stop=True)
