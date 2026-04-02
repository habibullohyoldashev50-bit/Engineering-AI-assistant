import telebot
import anthropic
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

SYSTEM_PROMPT = "Sen fizika va muhandislik sohasidagi mutaxassis AI yordamchisisan. Faqat shu sohalar boyicha savollarga javob ber. Boshqa mavzularda: Uzr, men faqat fizika va muhandislik boyicha yordam bera olaman de. Uzbek tilida javob ber."

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men fizika va muhandislik boyicha AI yordamchiman! Menga savol bering. 🔬⚙️")

@bot.message_handler(func=lambda m: True)
def handle(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.content[0].text)
    except Exception as e:
        bot.reply_to(message, f"Xatolik: {str(e)}")