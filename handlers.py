from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from questions import new_quiz


async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Начать игру'))
    await message.answer('Добро пожаловать в квиз!', reply_markup=builder.as_markup(resize_keyboard=True))


async def cmd_quiz(message: types.Message):
    await message.answer('Давайте начнем квиз!')
    await new_quiz(message)


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command('start'))
    dp.message.register(cmd_quiz, Command('quiz'))
    dp.message.register(cmd_quiz, lambda message: message.text == 'Начать игру')
