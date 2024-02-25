from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '6470319699:AAFZAv2AulBCohVSY4HVkKschZcJwudnjPs'
bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start']) #Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ Эхо-бот от Skillbox!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")
