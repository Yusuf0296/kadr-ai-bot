
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! Men Kadr AI agentiman. "
        "Xodimlar va hujjatlar bilan ishlashga yordam beraman."
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.responses.create(
        model="gpt-5-mini",
        instructions="""
Sen Kadr AI agentisan.
Vazifang:
- xodimlar bilan bog‘liq ma’lumotlarni tahlil qilish;
- hujjatlarni tekshirish;
- xodimlar ro‘yxati va jadvallar bilan ishlash;
- kamchiliklarni aniqlash;
- rahbarga tushunarli va amaliy natija berish.

Javoblarni o‘zbek tilida, aniq va amaliy ber.
""",
        input=user_text
    )

    await update.message.reply_text(response.output_text)


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()


if __name__ == "__main__":
    main()
