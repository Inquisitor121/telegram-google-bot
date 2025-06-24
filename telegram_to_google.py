import os
import json
import telebot
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Загружаем токены и ключи из переменных среды
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Подгружаем credentials.json из секретного файла Render
with open("/etc/secrets/credentials.json") as f:
    creds_dict = json.load(f)

# Настройка доступа к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("ТС-Энерго Бот").worksheet("Лист6")

# Настройка телеграм-бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши сообщение в формате:\n"
                          "`Сумма / Статья / Контрагент / Комментарий / Объект`\n"
                          "и я сохраню его в таблицу.",
                 parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user = message.from_user.first_name
    date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    text = message.text.strip()
    
    parts = [p.strip() for p in text.split("/")]

    # Дополняем до 5 частей если чего-то не хватает
    while len(parts) < 5:
        parts.append("")

    row = [user, date] + parts[:5]
    sheet.append_row(row)
    bot.reply_to(message, "✅ Сохранил в таблицу!")

print("Бот запущен и ожидает сообщения...")
bot.polling()
