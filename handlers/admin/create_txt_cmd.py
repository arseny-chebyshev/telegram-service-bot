import os.path
from loader import dp
from settings import admin_id

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from states.admin import AdminStates
from ..user import custom_handlers


class TxtCmd(StatesGroup):
    inserting_txt_cmd = State()
    inserting_txt_reply = State()


@dp.message_handler(Text(equals=['ADD TEXT CMD']), state=AdminStates.admin_state)
async def add_text_cmd(msg: Message):
    await msg.answer(text="Insert new function:", reply_markup=ReplyKeyboardRemove())
    await TxtCmd.inserting_txt_cmd.set()


@dp.message_handler(state=TxtCmd.inserting_txt_cmd)
async def insert_cmd_text(msg: Message, state: FSMContext):
    await state.update_data({'cmd': msg.text})
    await msg.answer(f'''Message {(await state.get_data('cmd'))['cmd']} taken as command.\nInsert reply:''')
    await TxtCmd.inserting_txt_reply.set()


@dp.message_handler(state=TxtCmd.inserting_txt_reply)
async def insert_reply_text(msg: Message, state: FSMContext):
    await state.update_data({'reply': msg.text})
    data = await state.get_data()
    await msg.answer(f"""Message {data['reply']} taken as reply.\nType /finish to apply command, and restart the bot!""")
    await AdminStates.admin_state.set()


@dp.message_handler(Command('finish'), state=AdminStates.admin_state)
async def save_text_cmd(msg: Message, state: FSMContext):
    if int(msg.from_user.id) == int(admin_id):
        try:
            data = await state.get_data()
            script = f"@dp.message_handler(Command('{data['cmd']}'))\nasync def x(msg: Message):\n    await msg.answer(text='{data['reply']}')\n\n\n"
            await state.reset_state(with_data=True)
            with open(os.path.abspath(custom_handlers.__file__), 'a', encoding='utf-8') as f:
                f.write(script)
                f.close()

        except KeyError:
            await msg.answer("Use ADD TEXT CMD interface to set the command first")

    else:
        await msg.answer("No admin rights to do that. Sorry!")
