from aiogram import Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from db import get_user_stats, update_quiz_index
from questions import quiz_data


async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Начать игру'))
    await message.answer(
        f'Добро пожаловать в квиз!\nДля начала игры нажмите кнопку "Начать игру"',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


async def cmd_quiz(message: types.Message):
    await message.answer('Давайте начнем квиз!')
    await new_quiz(message)


async def new_quiz(message: types.Message):
    user_id = message.from_user.id
    await update_quiz_index(user_id, 0, 0)
    await get_question(message, user_id)


async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    current_question_index, point = await get_user_stats(user_id)
    if current_question_index >= len(quiz_data):
        await message.answer(f'Ваш последний результат: {point} из {len(quiz_data)}')
    else:
        await message.answer(f'Для отображения статистики завершите текущий квиз')


def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(
            types.InlineKeyboardButton(
                text=option, callback_data='right_answer' if option == right_answer else 'wrong_answer'
            )
        )
    builder.adjust(1)
    return builder.as_markup()


async def get_question(message: types.Message, user_id: int):
    current_question_index, point = await get_user_stats(user_id)
    correct_option = quiz_data[current_question_index]['correct_option']
    options = quiz_data[current_question_index]['options']
    keyboard = generate_options_keyboard(options, options[correct_option])
    await message.answer(quiz_data[current_question_index]['question'], reply_markup=keyboard)


async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id, message_id=callback.message.message_id, reply_markup=None
    )

    await callback.message.answer('Верно!')
    current_question_index, point = await get_user_stats(callback.from_user.id)
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    # увеличиваем счетчик правильных ответов
    point = +1

    await update_quiz_index(callback.from_user.id, current_question_index, point)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer('Это был последний вопрос. Квиз завершен!')


async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id, message_id=callback.message.message_id, reply_markup=None
    )

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index, point = await get_user_stats(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    await callback.message.answer(
        f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}"
    )

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index, point)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer('Это был последний вопрос. Квиз завершен!')


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command('start'))
    dp.message.register(cmd_quiz, Command('quiz'))
    dp.message.register(cmd_stats, Command('stats'))
    dp.message.register(cmd_quiz, F.text == 'Начать игру')
    dp.callback_query.register(right_answer, F.data == 'right_answer')
    dp.callback_query.register(wrong_answer, F.data == 'wrong_answer')
