from loader import dp
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from states.fsm_test import FsmTest


@dp.message_handler(Command('fsm'), state=None)
async def start_fsm_test(msg: Message):
    await msg.answer('''Okay, let's start.\n#1: How are you today?''')
    await FsmTest.Q1.set()


@dp.message_handler(state=FsmTest.Q1)
async def answer_fsm_q1(msg: Message, state: FSMContext):
    await state.update_data({'answer1': msg.text})
    await msg.answer(f'''Message {(await state.get_data('answer1'))['answer1']}
taken as answer.\n#2: How's your mama?''')
    await FsmTest.Q2.set()


@dp.message_handler(state=FsmTest.Q2)
async def answer_fsm_q2(msg: Message, state: FSMContext):
    await state.update_data({'answer2': msg.text})
    await state.reset_state(with_data=False)
    await msg.answer("That's all I needed to know! Type /result to see your answers")


@dp.message_handler(Command('result'))
async def send_result(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.reset_data()
    await msg.answer(f'''Here are your answers:\n
#1: How are you today?  <b>{data['answer1']}</b>\n
#2: How's your mama?  <b>{data['answer2']}</b>''')
