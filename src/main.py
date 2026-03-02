import asyncio
import logging

from telebot.async_telebot import AsyncTeleBot
import llm
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
    text = 'Привет! Я юридический ИИ-помощник. Начнем общение' if message.text == '/start' else 'Начнем сначала'

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
        llm_response = await llm.handle_user_request(message.text)

        await bot.send_chat_action(message.chat.id, "typing")
        await bot.delete_message(message.chat.id, wait_message.message_id)
        await bot.send_message(message.chat.id, llm_response)
    except Exception as e:
        logging.error(e)
        await bot.delete_message(message.chat.id, wait_message.message_id)
        await bot.send_message(message.chat.id, 'Ваш запрос не может быть обработан. Попробуйте еще разок')


async def debug_llm() -> None:
    res = await llm.handle_user_request('Расскажи что такое УПК кратко')
    print(res)


if __name__ == '__main__':
    asyncio.run(set_main_menu())
    asyncio.run(bot.polling())
