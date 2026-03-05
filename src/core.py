import logging
import asyncio

from telebot.async_telebot import AsyncTeleBot
from model import llm
import config
from telebot.types import Message
from telebot import types

logging.basicConfig(level=logging.INFO)

bot = AsyncTeleBot(config.TELEGRAM_TOKEN)

buttons = {
    'start': 'Перезагрузка',
    'restart': 'Запуск',
}

@bot.message_handler(commands=buttons.keys())
async def send_message(message: Message):
    text = 'Привет! Я помощник по базе знаний. Начнем общение' if message.text == '/start' else 'Ок, Начнем сначала'

    await bot.send_message(message.chat.id, text)


async def set_main_menu():
    commands = []
    for name, value in buttons.items():
        commands.append(types.BotCommand(name, value))

    await bot.set_my_commands(commands)


@bot.message_handler(commands=['menu'])
async def show_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Start")
    btn2 = types.KeyboardButton("Restart")
    markup.add(btn1, btn2)

    await bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
async def handle_request(message: Message):
    wait_message = await bot.send_message(message.chat.id, "⏳ Ищу...")
    try:
        llm_response = await llm.send_message(user_input=message.text)

        await bot.send_chat_action(message.chat.id, "typing")
        await bot.delete_message(message.chat.id, wait_message.message_id)
        await bot.send_message(message.chat.id, llm_response)
    except Exception as e:
        logging.error(e)
        await bot.delete_message(message.chat.id, wait_message.message_id)
        await bot.send_message(message.chat.id, 'Неудачный запрос. Попробуй еще раз')


def run_bot() -> None:
    asyncio.run(set_main_menu())
    asyncio.run(bot.polling())
