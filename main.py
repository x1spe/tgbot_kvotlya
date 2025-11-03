import io
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from PIL import Image, ImageDraw, ImageFont
import os

TOKEN = os.getenv("BOT_TOKEN")  # токен берём из переменных окружения

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

FONT_PATH = "arial.ttf"

@dp.message_handler(commands=['q'])
async def make_quote(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Ответь на сообщение, чтобы сделать цитату 😉")
        return

    replied = message.reply_to_message
    text = replied.text or replied.caption or "(нет текста)"
    user = replied.from_user

    # Загружаем аватар
    photos = await bot.get_user_profile_photos(user.id)
    if photos.total_count > 0:
        photo = photos.photos[0][-1]
        file = await bot.get_file(photo.file_id)
        file_path = file.file_path
        avatar_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
        avatar = Image.open(io.BytesIO(requests.get(avatar_url).content)).convert("RGB")
        avatar = avatar.resize((100, 100))
    else:
        avatar = Image.new("RGB", (100, 100), (180, 180, 180))

    # Размер картинки под длину текста
    width = 600
    height = 180 + len(text)//25 * 25
    img = Image.new("RGB", (width, height), (245, 245, 245))
    draw = ImageDraw.Draw(img)

    # Вставляем аватар
    img.paste(avatar, (30, 30))

    # Имя пользователя
    font_name = ImageFont.truetype(FONT_PATH, 24)
    draw.text((150, 40), user.first_name, font=font_name, fill=(30, 30, 30))

    # Текст сообщения
    font_text = ImageFont.truetype(FONT_PATH, 22)
    draw.text((150, 80), text, font=font_text, fill=(50, 50, 50))

    # Сохраняем и отправляем
    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)

    await message.reply_photo(photo=output, caption="Цитата готова 🖼️")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
