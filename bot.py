import logging
import os
import base64
from aiogram import Bot, Dispatcher, types, executor
from openai import OpenAI

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(bot)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("OPENAI_PROJECT_ID"),
    organization=os.getenv("OPENAI_ORG_ID")
)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я — AI-Провидец. Отправь фото своей ладони для анализа (левая или правая).")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_hand_image(message: types.Message):
    await message.reply("Изображение получено. Выполняю хиромантический анализ...")
    photo = message.photo[-1]
    file_path = await photo.download(destination_dir=".")
    with open(file_path.name, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Ты — мастер-хиромант. Анализируй ладонь по фото, учитывая линии жизни, ума, сердца, судьбы, холмы. Дай подробный эзотерико-психологический разбор."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Вот фото моей ладони. Сделай полный анализ."
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
    except Exception as e:
        await message.reply(f"Ошибка: {str(e)}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
