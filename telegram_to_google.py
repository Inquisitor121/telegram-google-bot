import os
import json
import telebot
import gspread
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# ─── Запуск фейкового HTTP-сервера ────────────────────────
def keep_alive():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

keep_alive()

# ─── Авторизация Google Sheets ─────────────────────────────
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

with open("/etc/secrets/credentials.json") as f:
    creds_dict = json.load(f)

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet = client.open("ТС-Энерго Бот").worksheet("Лист6")

# ─── Настройка Telegram бота ──────────────────────────────
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши мне данные через `/`, и я сохраню их в таблицу Google Sheets.\nФормат:\n`1000 / Статья / Контрагент / Комментарий / Объект`")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user = message.from_user.first_name
    date = datetime.now().strftime("%d.%m.%Y")  # только дата
    parts = [p.strip() for p in message.text.split("/")]

    while len(parts) < 5:
        parts.append("")

    row = [user, date] + parts[:5]
    sheet.append_row(row)
    bot.reply_to(message, "✅ Сохранил!")

print("Бот запущен и ожидает сообщения...")
bot.polling()
