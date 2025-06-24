import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json
import re

# Загрузка credentials
creds_dict = json.loads(os.environ["GOOGLE_CREDS"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("ТС-Энерго Бот").worksheet("Лист6")

bot = telebot.TeleBot(os.environ["TELEGRAM_TOKEN"])

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    username = message.from_user.first_name or "Неизв."
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = message.text.strip()

    # Разбиваем по разделителю '/'. Убираем лишние пробелы.
    parts = [part.strip() for part in re.split(r'\s*/\s*', text)]

    # Обеспечим минимум 5 частей (Сумма, Статья, Контрагент, Комментарий, Объект)
    parts += [""] * (5 - len(parts))
    parts = parts[:5]

    row = [username, timestamp] + parts
    sheet.append_row(row)
    bot.reply_to(message, "✅ Записано: " + " | ".join(parts))

bot.polling()
