from aiogram import Bot,types
from aiogram.dispatcher import Dispatcher,FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data_base import sql_database
from aiogram.dispatcher.filters import Text
import os
bot=Bot(token=os.getenv("TOKEN"))
storage=MemoryStorage()
dp=Dispatcher(bot,storage=storage)
class MGE(StatesGroup):
    photo=State()
help_button=KeyboardButton("/help")
MGE_button=KeyboardButton("/MGE")
MGE_download_button=KeyboardButton("/MGE_загрузка")
MGE_otmena=KeyboardButton("/отмена")
proverka_button=KeyboardButton("/проверка")
keyboard=ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row(help_button,MGE_button,MGE_download_button,MGE_otmena,proverka_button)
inline_yes=InlineKeyboardButton(text="да",callback_data="choice_yes")
inline_no=InlineKeyboardButton(text="нет",callback_data="choice_no")
inline_keyboard=InlineKeyboardMarkup(row_width=2)
inline_keyboard.row(inline_no,inline_yes)
async def on_startup(_):
    print("бот вышел онлайн")
    sql_database.db_connect()
@dp.message_handler(commands=["MGE_загрузка"],state=None)
async def MGE_start(message:types.Message):
    await MGE.photo.set()
    await message.answer("введи фото сосунок\n если передумал используй команду /отмена")
@dp.message_handler(commands=["отмена"],state="*")
async def MGE_otmena(message: types.Message,state: FSMContext):
    current_state=await state.get_state()
    if current_state is None:
        return None
    else:
        await message.answer("команда отменена")
        await state.finish()
@dp.message_handler(content_types=["photo"],state=MGE.photo)
async def MGE_work(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data["photo"]=message.photo[0].file_id
        photo_id=data["photo"]
    await sql_database.sql_input(photo_id)
    await message.answer("готово сосунок")
    await state.finish()
@dp.message_handler(commands=["MGE"])
async def MGE_random(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,photo=sql_database.sql_send())
@dp.message_handler(commands=["проверка"])
async def proverka_start(message: types.Message):
    await message.answer("ты гей?",reply_markup=inline_keyboard)
@dp.message_handler(commands=["start","help"])
async def start_function(message: types.Message):
    await message.answer("Привет, я бот который может отправлять рандомную MGE превьюшку в чат по команде /MGE(вы также можете загружать превьюшки по команде /MGE_загрузки)",reply_markup=keyboard)
@dp.callback_query_handler(Text(startswith="choice_"))
async def proverka(call: types.CallbackQuery):
    if call.data.split("_")[1]=="yes":
        await call.message.answer("ебать ты пидор")
        await call.answer("пидор",show_alert=True)
    else:
        await call.message.answer("пидора ответ")
        await call.answer()
executor.start_polling(dp,skip_updates=True,on_startup=on_startup)