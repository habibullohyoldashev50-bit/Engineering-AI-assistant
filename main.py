import telebot
import anthropic
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

SYSTEM_PROMPT = """Sen fizika va muhandislik (engineering) sohasidagi mutaxassis AI yordamchisisan. Faqat shu sohalar bo'yicha savollarga javob ber. Boshqa mavzularda: 'Uzr, men faqat fizika va muhandislik bo'yicha yordam bera olaman' de. O'zbek tilida javob ber."""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! 👋 Men fizika va muhandislik bo'yicha AI yordamchiman!\n\nMenga savol bering, javob beraman. 🔬⚙️")

@bot.message_handler(func=lambda m: True)
def handle(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.content[0].text)
    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi, qayta urinib ko'ring.")

bot.polling()
