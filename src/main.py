import asyncio
import logging

from telebot.async_telebot import AsyncTeleBot
import llm
import config
from telebot.types import Message
from telebot import types
from confluence.confluence_mcp import mcp_request

logging.basicConfig(level=logging.INFO)

bot = AsyncTeleBot(config.TELEGRAM_TOKEN)

buttons = {
    'start': 'Перезагрузка',
    'restart': 'Запуск',
}


@bot.message_handler(commands=buttons.keys())
async def send_message(message: Message):
    text = 'Привет! Я помощник по базе знаний. Начнем общение' if message.text == '/start' else 'Начнем сначала'

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
    wait_message = await bot.send_message(
        message.chat.id,
        "⏳ Ждем ответ..."
    )
    try:
        data_from_confluence = mcp_request(message.text)

        llm_response = await llm.handle_user_request(
            user_input=message.text,
            data_from_database=data_from_confluence
        )

        await bot.send_chat_action(message.chat.id, "typing")
        await bot.delete_message(message.chat.id, wait_message.message_id)
        await bot.send_message(message.chat.id, llm_response)
    except Exception as e:
        logging.error(e)
        await bot.delete_message(message.chat.id, wait_message.message_id)
        await bot.send_message(message.chat.id, 'Ваш запрос не может быть обработан. Попробуйте еще разок')


if __name__ == '__main__':
    asyncio.run(set_main_menu())
    asyncio.run(bot.polling())
