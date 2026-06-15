import os
import asyncio
import base64
import aiohttp
import logging
from groq import Groq
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart

from example import example


# Start Flask web server thread
example()

# Telegram Bot Token
BOT_TOKEN = "8873104622:AAGft8nftlIxAsiQAg0QoaDU8JkWAp-CTKQ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Create Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# OR use environment variable:
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))
print("GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Hello! I am GPT Chat Bot 🤖\n\nAsk me anything!")


@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("Send me any message and I'll reply using AI.")


@dp.message()
async def gpt(message: types.Message):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message.text},
            ],
        )

        reply = response.choices[0].message.content

        await message.reply(reply)

        print("Response:", response)

    except Exception as e:
        print("ERROR:", e)
        await message.reply(f"Error: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
