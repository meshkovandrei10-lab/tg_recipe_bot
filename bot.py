print("🤖 Recipe Bot + Render HTTP!")
import telebot
import requests
import os
from dotenv import load_dotenv
from flask import Flask
import threading
import time

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
NUTRITION_KEY = os.getenv('NUTRITION_API_KEY')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 🔥 HTTP для Render (ОБЯЗАТЕЛЬНО!)
@app.route('/')
@app.route('/health')
def health():
    return {'status': 'Telegram Recipe Bot OK!', 'time': time.time()}

# Telegram команды
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "🎉 *Recipe Bot готов!*\n\n"
        "🍗 Пиши продукты с весом:\n"
        "`курица 200г`\n`рис 100г`\n`яйца 2шт`\n\n"
        "🍽️ Примеры:\n"
        "`ужин 500ккал`\n`творог 150г`", parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def nutrition(message):
    query = message.text.strip()
    
    url = f'https://api.calorieninjas.com/v1/nutrition?query={query}'
    headers = {'X-Api-Key': NUTRITION_KEY}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()['items']
        
        if data:
            item = data[0]
            text = f"""✅ *{query}*

🍗 **{item['name'].title()}**
📏 **{item['serving_size_g']}г**

**БЖУ на порцию:**
• 🥚 Белки: **{item['protein_g']}г**
• 🥑 Жиры: **{item['fat_total_g']}г**
• 🍞 Углеводы: **{item['carbohydrates_total_g']}г**
• 🔥 Калории: **{item['calories']} ккал**"""
            bot.reply_to(message, text, parse_mode='Markdown')
        else:
            bot.reply_to(message, f"❓ Не нашёл `{query}`\n\nПример: `курица 200г`", parse_mode='Markdown')
            
    except Exception as e:
        bot.reply_to(message, 
            f"❌ Ошибка: {str(e)[:50]}\n\n"
            f"✅ Попробуй: `курица грудка 200г`\n"
            f"`рис 100г`\n`яйца 2шт`", parse_mode='Markdown')

def run_bot():
    print("🚀 Telegram бот запущен!")
    bot.infinity_polling()

def run_flask():
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 HTTP сервер на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    print("🎉 Бот + HTTP работают!")
    flask_thread.join()
