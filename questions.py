from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import get_quiz_index, update_quiz_index


quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0,
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0,
    },
]


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
    current_question_index = await get_quiz_index(user_id)
    correct_option = quiz_data[current_question_index]['correct_option']
    options = quiz_data[current_question_index]['options']
    keyboard = generate_options_keyboard(options, options[correct_option])
    await message.answer(quiz_data[current_question_index]['question'], reply_markup=keyboard)


async def new_quiz(message: types.Message):
    user_id = message.from_user.id
    await update_quiz_index(user_id, 0)
    await get_question(message, user_id)


async def handle_right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id, reply_markup=None)
    await callback.message.answer('Верно!')
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer('Это был последний вопрос. Квиз завершен!')


async def handle_wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id, reply_markup=None)
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    await callback.message.answer(
        f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}"
    )
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer('Это был последний вопрос. Квиз завершен!')
