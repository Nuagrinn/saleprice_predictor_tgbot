from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, ContentTypeFilter
import buttons as btn
import logging
from app import dp
from states import Test
from ml_functions import make_one_prediction


@dp.callback_query_handler(text='cancel')
async def cancel_answer(call: CallbackQuery):
    logging.info(call.data)
    await call.message.edit_reply_markup()


@dp.message_handler(Command('start'), state=None)
async def show_items(message: Message):
    logging.info(f'Bot started')
    await message.answer(text='Привет! Этот бот поможет вам рассчитать цену на вторичную квартиру в Москве. \n'
                              'Но для этого он должен знать некоторые ее характеристики. '
                              'Вам нужно будет ответить на 8 вопросов. Данные деперсонализованны '
                              'и удаляются сразу после выдачи результатов. \n'
                              'Важно: точность расчетов сильно завит от того, насколько корректно вы введете данные. \n'
                              'Если вы готовы, мы можем начать',
                         reply_markup=btn.start_choice)


@dp.callback_query_handler(btn.start_callback.filter(choice_status='yes'), state=None)
async def question_one(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(call.data)
    await call.message.answer('Отлично. Сперва введите улицу и номер дома, \n'
                              'Пример: ул. Большая Ордынка, 56')
    await Test.Q1.set()


@dp.message_handler(state=Test.Q1)
async def answer_q1(message: Message, state: FSMContext):
    answer = message.text
    logging.info(f"address: {answer}")

    async with state.proxy() as data:
        data['address'] = answer
    await message.answer('Теперь необходимо ввести площадь квартиры в квадратных метрах. \n'
                         'Пример: 56,3')
    await Test.next()


@dp.message_handler(state=Test.Q2)
async def answer_q1(message: Message, state: FSMContext):
    answer = message.text
    logging.info(f"total_area: {answer}")

    async with state.proxy() as data:
        data['total_area'] = answer
    await message.answer('Сколько комнат в квартире?\n'
                         'Введите число от 1-5 или 6, если в квартире больше 5 комнат')
    await Test.next()


@dp.message_handler(state=Test.Q3)
async def answer_q2(message: Message, state: FSMContext):
    answer = message.text
    logging.info(f"numofrooms: {answer}")

    async with state.proxy() as data:
        data['numofrooms'] = answer
    await message.answer('Если рядом есть метро, можно ли до него дойти пешком \n'
                         'за 15-20 минут или меньше? Если метро рядом нет, выберите "Нет"',
                         reply_markup=btn.q3_choice)
    await Test.next()


@dp.callback_query_handler(btn.q3_callback.filter(choice_status='yes'), state=Test.Q4)
async def answer_q3(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    answer = callback_data.get('choice_status')
    logging.info(f"walkmetroaccess: {answer}")

    async with state.proxy() as data:
        data['walkmetroaccess'] = answer
    await call.message.answer("Год постройки дома в формате ГГГГ? \n"
                              "Пример: 1968")

    await Test.next()


@dp.callback_query_handler(btn.q3_callback.filter(choice_status='no'), state=Test.Q4)
async def answer_q3(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    answer = callback_data.get('choice_status')
    logging.info(f"walkmetroaccess: {answer}")

    async with state.proxy() as data:
        data['walkmetroaccess'] = answer
    await call.message.answer("Год постройки дома в формате ГГГГ? \n"
                              "Пример: 1968")

    await Test.next()


@dp.message_handler(state=Test.Q5)
async def answer_q4(message: Message, state: FSMContext):
    answer = message.text
    logging.info(f"constryear: {answer}")

    async with state.proxy() as data:
        data['constryear'] = answer
    await message.answer('Сейчас нужно определиться с типом жилья',
                         reply_markup=btn.q5_choice)

    await Test.next()


@dp.callback_query_handler(btn.q5_callback.filter(accom_type='flat'), state=Test.Q6)
async def answer_q5(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    answer = callback_data.get('accom_type')
    logging.info(f"accom_type: {answer}")

    async with state.proxy() as data:
        data['accomtype'] = answer
    await call.message.answer("Какой тип ремонта?",
                              reply_markup=btn.q6_choice)

    await Test.next()


@dp.callback_query_handler(btn.q5_callback.filter(accom_type='apartment'), state=Test.Q6)
async def answer_q5(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    answer = callback_data.get('accom_type')
    logging.info(f"accom_type: {answer}")

    async with state.proxy() as data:
        data['accomtype'] = answer
    await call.message.answer("Какой тип ремонта?",
                              reply_markup=btn.q6_choice)

    await Test.next()


@dp.callback_query_handler(btn.q5_callback.filter(accom_type='penthouse'), state=Test.Q6)
async def answer_q5(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    answer = callback_data.get('accom_type')
    logging.info(f"accom_type: {answer}")

    async with state.proxy() as data:
        data['accomtype'] = answer
    await call.message.answer("Какой тип ремонта?",
                              reply_markup=btn.q6_choice)

    await Test.next()


@dp.callback_query_handler(btn.q6_callback.filter(renov_type='light'), state=Test.Q7)
async def answer_q6(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    answer = callback_data.get('renov_type')
    logging.info(f"renov_type: {answer}")

    async with state.proxy() as data:
        data['renovtype'] = answer
    await call.message.answer("На каком этаже расположена квартира? \n"
                              "Пример: 2")

    await Test.next()


@dp.callback_query_handler(btn.q6_callback.filter(renov_type='design'), state=Test.Q7)
async def answer_q6(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    answer = callback_data.get('renov_type')
    logging.info(f"renov_type: {answer}")

    async with state.proxy() as data:
        data['renovtype'] = answer
    await call.message.answer("На каком этаже расположена квартира? \n"
                              "Пример: 2")

    await Test.next()


@dp.callback_query_handler(btn.q6_callback.filter(renov_type='euro'), state=Test.Q7)
async def answer_q6(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    answer = callback_data.get('renov_type')
    logging.info(f"renov_type: {answer}")

    async with state.proxy() as data:
        data['renovtype'] = answer
    await call.message.answer("На каком этаже расположена квартира? \n"
                              "Пример: 2")

    await Test.next()


@dp.callback_query_handler(btn.q6_callback.filter(renov_type='bare'), state=Test.Q7)
async def answer_q6(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    answer = callback_data.get('renov_type')
    logging.info(f'renov_type: {answer}')

    async with state.proxy() as data:
        data['renovtype'] = answer
    await call.message.answer("На каком этаже расположена квартира? \n"
                              "Пример: 2")

    await Test.next()


@dp.message_handler(state=Test.Q8)
async def answer_q7(message: Message, state: FSMContext):
    answer = message.text
    logging.info(f'floornum: {answer}')

    async with state.proxy() as data:
        data['floornum'] = answer
    await message.answer('И последнее. Сколько всего этажей в доме? \n'
                         'Пример: 5')

    await Test.next()


@dp.message_handler(state=Test.Q9)
async def answer_q8(message: Message, state: FSMContext):
    answer = message.text

    async with state.proxy() as data:
        data['flooramnt'] = answer

    data = await state.get_data()
    predicted_price = make_one_prediction(data)
    await message.answer(f'Вот что мы получили: {predicted_price} '
                         f'Попробуем еще раз или закончим?',
                         reply_markup=btn.start_choice)
    logging.info(f'flooramnt:{answer} and prediction {predicted_price}.')

    await state.finish()


@dp.message_handler()
async def answer_error(message: Message):
    answer = message.text
    logging.info(f"user message: {answer}")

    await message.answer('Данные введены некорректно, либо бот не понимает вашего сообшения. '
                         'Попробуйте еще раз.')
