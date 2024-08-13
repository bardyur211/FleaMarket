import asyncio
import logging
import sys
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ContentType, Message, CallbackQuery, KeyboardButton, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods import DeleteMessage



# Config logging
logging.basicConfig(level=logging.INFO)

# BOt token and dispatcher
BOT = Bot(token='7473178796:AAEbEg2wkTTzrnLtQbo-U22rUqhndZzGJzs')
dp = Dispatcher()


class AddWordBList(StatesGroup):
    word = State()

class DelWordBList(StatesGroup):
    word = State()

#class JUSTIFY(StatesGroup):
#    text = State()

@dp.message(Command('add_blacklist'))
async def add_blacklist(message: Message, state: FSMContext):
    await state.set_state(AddWordBList.word)
    await message.reply('Напишите слово которое хотите занести в черный список')

@dp.message(AddWordBList.word)
async def add_blacklist(message: Message, state: FSMContext):
    text = message.text.lower()
    con = sqlite3.connect('blacklist.db')
    cursor = con.cursor()
    cursor.execute("INSERT INTO Words (Word) VALUES (?)", (text,))
    con.commit()
    con.close()
    await message.reply(f'Слово {message.text} добавлено в черный список')
    await state.clear()

@dp.message(Command('del_blacklist'))
async def del_blacklist(message: Message, state: FSMContext):
    await state.set_state(DelWordBList.word)
    await message.reply('Напишите слово которое хотите удалить из черного списка')

@dp.message(DelWordBList.word)
async def del_blacklist(message: Message, state: FSMContext):
    text = message.text.lower()
    con = sqlite3.connect('blacklist.db')
    cursor = con.cursor()
    cursor.execute("DELETE FROM Words WHERE Word = ?", (text,))
    con.commit()
    con.close()
    await message.reply(f'Слово {message.text} удалено из черного списка')
    await state.clear()

@dp.message(Command('justify'))
async def justify_0(message: Message, fsm: FSMContext):
    print(message.from_user.id)

@dp.message(F.text)
async def check_blacklist(message: Message, bot: BOT):
    text = message.text.lower().split(' ')
    con = sqlite3.connect('blacklist.db')
    cursor = con.cursor()
    for i in text:
        cursor.execute("SELECT Word FROM Words WHERE Word = ?", (i,))
        data = cursor.fetchall()
        if data:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await message.answer('Подозрение в нарушении УК РФ')
            break
        else:
            pass
    con.close()



async def main():
    await dp.start_polling(BOT)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())