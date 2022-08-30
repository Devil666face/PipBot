import config

from pathlib import Path
from aiogram import Bot,Dispatcher,types,executor
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

from core import PipLoader
from markup import keyboard_main

bot = Bot(token=config.TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

@dp.message_handler(commands = ['start'],state=None)
async def start(message: types.Message):
    await message.answer('Welcome. Send me the name of pip package, and i send you all extensions of this pack.',reply_markup=keyboard_main)

async def send_separeted_files(message, files, pack_dir):
    for file in files:
        try:
            await message.answer_document(open(Path(pack_dir,file),'rb'))
        except Exception as ex:
            await message.answer('I dont send file more then 40 mB.')
            print(ex)

async def send_document(message, acrhive_name, files, pack_dir):
    try:
        await message.answer_document(open(acrhive_name,'rb'))
    except:
        await send_separeted_files(message, files, pack_dir=pack_dir)
        
@dp.message_handler(Text(equals='Get Python'))
async def get_python(message: types.Message, state: FSMContext):
    await message.answer('<a href="https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe">Python 3.10</a>',parse_mode='html')


@dp.message_handler(content_types=['text'],state=None)
async def download_pack(message: types.Message, state:FSMContext):
    try:
        await message.answer(f'Start to downloading all extensions for "{message.text}" please await...',reply_markup=keyboard_main)
        loader =  PipLoader(message.text)
        files, acrhive_name = loader.get_files()
        await send_document(message, acrhive_name, files, pack_dir=loader.pack_dir)
        await message.answer(f'1. Unpack this archive in your project on the same level with venv.\n2. Use this command to install extensions: {loader.get_command()}\n3. This packeges supports only python 3.10 and over.',reply_markup=keyboard_main)
        del loader
        
    except Exception as ex:
        await message.answer(f'Oops... something went wrong.\nThe error code: {ex}',reply_markup=keyboard_main)

if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)