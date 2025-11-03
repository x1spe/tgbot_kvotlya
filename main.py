try:
    import imghdr
except ModuleNotFoundError:
    import filetype as imghdr

import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Токен из переменной окружения (Render -> Environment)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Функция для создания картинки-цитаты
def make_quote_image(name: str, text: str, avatar_url: str = None):
    # Загружаем аватар или создаём заглушку
    try:
        if avatar_url:
            avatar_bytes = requests.get(avatar_url).content
            avatar = Image.open(BytesIO(avatar_bytes)).resize((100, 100))
        else:
            avatar = Image.new("RGB", (100, 100), (200, 200, 200))
    except Exception:
        avatar = Image.new("RGB", (100, 100), (200, 200, 200))

    # Создаём базовое изображение
    img = Image.new("RGB", (600, 200), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Вставляем аватар
    img.paste(avatar, (30, 50))

    # Текст и ник
    font = ImageFont.load_default()
    draw.text((150, 60), name, fill=(0, 0, 0), font=font)
    draw.text((150, 90), text, fill=(60, 60, 60), font=font)

    # Сохраняем
    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output


# Обработка команды /q или q
def quote(update: Update, context: CallbackContext):
    message = update.message

    if message.reply_to_message:
        replied = message.reply_to_message
        user = replied.from_user
        name = user.full_name
        text = replied.text or replied.caption or "<без текста>"

        # Получаем аватар
        avatar_url = None
        try:
            photos = user.get_profile_photos(limit=1).photos
            if photos:
                file = context.bot.get_file(photos[0][0].file_id)
                avatar_url = file.file_path
        except Exception:
            pass

        # Генерация изображения
        img = make_quote_image(name, text, avatar_url)
        message.reply_photo(photo=InputFile(img), caption=f"💬 Цитата от {name}")
    else:
        message.reply_text("Ответь на сообщение, чтобы создать цитату 😉")


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Команда /q
    dp.add_handler(CommandHandler("q", quote))

    # Реакция на просто "q" без слэша
    dp.add_handler(MessageHandler(Filters.regex(r'^(?i)q$'), quote))

    updater.start_polling()
    print("✅ Бот запущен и работает 24/7")
    updater.idle()


if __name__ == "__main__":
    main()
