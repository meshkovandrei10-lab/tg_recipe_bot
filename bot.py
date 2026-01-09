print("🤖 Бот запускается!")
import telebot
import os
from dotenv import load_dotenv
load_dotenv()
bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
print("✅ Бот подключён!")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎉 БОТ РАБОТАЕТ!\nПиши: курица 200г")

@bot.message_handler(func=lambda m: True)
def bju(message):
    import requests
    query = message.text
    headers = {'X-Api-Key': os.getenv('NUTRITION_API_KEY')}
    url = f'https://api.calorieninjas.com/v1/nutrition?query={query}'
    try:
        r = requests.get(url, headers=headers)
        data = r.json()['items'][0]
        text = f"✅ {query}\n{data['name']}\n{data['serving_size_g']}г\nБ:{data['protein_g']}г Ж:{data['fat_total_g']}г У:{data['carbohydrates_total_g']}г\n{data['calories']}ккал"
        bot.reply_to(message, text)
    except:
        bot.reply_to(message, f"Пример: {query} курица рис")

bot.infinity_polling()
