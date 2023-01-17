import logging
import urllib

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, inline_keyboard, ParseMode

from Selenium import parser

API_TOKEN = 'token'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
data = dict()
data.setdefault("default", "")
defaultMessage: str = ""


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("""
        Привет!
        Я бот конвертор!
        Скинь мне номер или ссылку с krisha kz
        и я отправлю ссылку на чат в whatsUp.
        
        Команды:
        /help - напомнить что есть и могу
        /setdefault - заполнить сообщение по умолчанию
        """)


@dp.message_handler(commands=['setdefault'])
async def send_welcome1(message: types.Message):
    defaultMessage = message.text.replace("/setdefault ", "")
    data["default"] = defaultMessage
    await message.answer("Ваша сообщение по умолчанию " + defaultMessage)


BTN_WEATHER = InlineKeyboardButton('Weather', callback_data='weather')
BTN_WIND = InlineKeyboardButton('Wind', callback_data='wind')
BTN_SUN_TIME = InlineKeyboardButton('Sunrise and sunset',
                                    callback_data='sun_time')

WEATHER = InlineKeyboardMarkup().add(BTN_WIND, BTN_SUN_TIME)
WIND = InlineKeyboardMarkup().add(BTN_WEATHER).add(BTN_SUN_TIME)
SUN_TIME = InlineKeyboardMarkup().add(BTN_WEATHER, BTN_WIND)
HELP = InlineKeyboardMarkup().add(BTN_WEATHER, BTN_WIND).add(BTN_SUN_TIME)


@dp.message_handler(lambda message: message.text and 'http' in message.text.lower())
async def text_handler(message: types.Message):
    await message.reply("Придется подождать 2-3 минуты...")
    tns: str = parser(message.text)
    for tn in tns:
        await message.reply(converter(tn), reply_markup=inline_keyboard.WEATHER)


@dp.message_handler()
async def echo(message: types.Message):
    try:
        message_to_answer = converter(message.text)
    except:
        message_to_answer = "не смог обработать"
    await message.reply(message_to_answer, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def converter(text):
    if text.__eq__("что пошло не так проверьте правильность сслыки"):
        return text
    if text.startswith("8"):
        text = '7' + text[1:]
    new_string = text.replace(" ", "").replace("(", "").replace(")", "").replace("+", "").replace("-", "")
    if data["default"] == "":
        return "https://wa.me/" + new_string
    else:
        return "https://wa.me/" + new_string +"?text="+urllib.parse.quote_plus(data["default"])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
