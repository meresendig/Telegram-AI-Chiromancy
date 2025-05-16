# AI-Провидец (Project API) — Модуль Хиромантии

## Инструкция для Render

1. Создай переменные окружения:
- TELEGRAM_BOT_TOKEN = Токен от BotFather
- OPENAI_API_KEY = sk-svcacct-...
- OPENAI_PROJECT_ID = prj_...
- OPENAI_ORG_ID = org_...

2. Build command:
pip install -r requirements.txt

3. Start command:
python bot.py

## Что делает бот:
- Принимает изображение ладони
- Отправляет запрос в GPT-4o с изображением
- Возвращает эзотерический анализ
