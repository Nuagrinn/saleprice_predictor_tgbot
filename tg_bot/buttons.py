from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

start_callback = CallbackData('choice', 'choice_status')
start_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Поехали!', callback_data=start_callback.new(
                choice_status='yes')),
        ],
        [
            InlineKeyboardButton(text='Отменить', callback_data="cancel")
        ]
    ]
)

q3_callback = CallbackData('choice', 'choice_status')
q3_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data=q3_callback.new(
                choice_status='yes')),
            InlineKeyboardButton(text='Нет', callback_data=q3_callback.new(
                choice_status='no'))
        ]
    ]
)

q5_callback = CallbackData('choice', 'accom_type')
q5_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Вторичка', callback_data=q5_callback.new(
                accom_type='flat')),
            InlineKeyboardButton(text='Апартаменты', callback_data=q5_callback.new(
                accom_type='apartment'))
        ],
        [
            InlineKeyboardButton(text='Пентхаус', callback_data=q5_callback.new(
                accom_type='penthouse'))
        ]
    ]
)

q6_callback = CallbackData('choice', 'renov_type')
q6_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Косметический', callback_data=q6_callback.new(
                renov_type='light')),
            InlineKeyboardButton(text='Дизайнерский', callback_data=q6_callback.new(
                renov_type='design'))
        ],
        [
            InlineKeyboardButton(text='Евроремонт', callback_data=q6_callback.new(
                renov_type='euro')),
            InlineKeyboardButton(text='Без ремонта', callback_data=q6_callback.new(
                renov_type='bare'))
        ]
    ]
)

