import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ContentType
from openai import OpenAI
import os
import base64

API_TOKEN = os.getenv("API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

client = OpenAI(api_key=OPENAI_API_KEY)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь фото ладони (левой или правой), и я пришлю тебе хиромантический анализ.")

@dp.message_handler(content_types=ContentType.PHOTO)
async def handle_photo(message: types.Message):
    await message.reply("Фото получено. Обрабатываю...")
    photo = message.photo[-1]
    file_path = await photo.download(destination_dir=".")
    
    with open(file_path.name, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Ты — опытный хиромант. Проанализируй ладонь на изображении. Учитывай линии жизни, головы, сердца, судьбы, а также холмы и форму руки. Составь детальный психологический, судьбоносный и энергетический разбор."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Вот фото моей ладони. Дай полный разбор по канонам хиромантии."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000
    )

    await message.reply(response.choices[0].message.content)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)