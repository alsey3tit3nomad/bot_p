Token = "6983222662:AAHuL3mPbvI_Pm9BcD17R4bUBk8uFqVVVho"
# Token = '7130681319:AAG6JADBaqM3qD_dEREbGcV9rRkFL0Q0O7M'
import asyncio
from asyncio import sleep
from aiogram.types import message
import pandas as pd
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
# from PyPDF2 import PdfReader
bot = Bot(token=Token)
dp = Dispatcher()

students_names = {}
students_id = {}
def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

@dp.message(CommandStart())
async def on_message(message):
    await message.answer(f"привет, {message.from_user.first_name}.")
    await sleep(1)
    await message.answer(f"Чтобы попасть на самое таинственное мероприятие этой весны, нужно всего-то ничего...\n\nУкажите свое полное ФИО, чтобы продолжить процесс {strike('Кафки')} покупки билетов на метаПосвят | похороны политфака.")
    await message.delete()


@dp.message()
async def handle_FIO(message):
  global students_names, students_id
  if (message.document == None and message.photo == None and message.text[:5] != 'https'):
    print(message)
    if (str(message.text)[:6] != "/mtdm_" and str(message.text) != "/result"):
      FIO = str(message.text)
      students_names[FIO] = [message.from_user.id, "no"]
      students_id[message.from_user.id] = FIO
      await bot.send_message(chat_id=-1002146003569, text=f'@{message.from_user.username}')
      await message.answer("Далее перечислите стоимость билета 1800р на удобный вам банк:\n\nЕва З.П. — 5536914056119104 — ТИНЬКОФФ\nТимур Х.А. — 2202206721668189 — СБЕР\n\nА затем пришлите либо чек(!) об оплате либо в формате документа, либо фотографией.")
    elif (str(message.text)[:6] == "/mtdm_"):
      mes_inf = str(message.text).strip("/mtdm_")
      mes_inf = mes_inf.split("_")
      name = mes_inf[0]
      n_sum = int(mes_inf[1])
      students_names[name][1] = n_sum
      with open("file.txt", "w") as file:
        file.write(str(name + "," + str(n_sum)+ "\n"))
      await bot.send_message(chat_id = students_names[name][0], text = "Оплата подтверждена!\nЖдём вас на метаПосвяте | похороны политфака.\n\n16.03.2024")
    else:
      mes_inf = str(message.text)
      string = ''
      for i in students_names.keys():
        if (type(students_names[i][1]) == int):
          string += i + ";" + str(students_names[i][1]) + "\n"
      await bot.send_message(chat_id=-1002146003569, text=string)


  else:
    print(message.document)
    await handle_pdf(message)

@dp.message()
async def handle_pdf(message):
  global students_names, students_id
  if (message.document == None or message.photo == None or message.text[:5] == 'https'):
    try:
      students_names[students_id[message.from_user.id]][1] = "wait"
      await message.answer("Ожидайте подтверждения оплаты.\n\nОрганизаторы метаПосвята не самые быстрые люди.\nДо конца рабочего дня ваша оплата будет подтверждена и мы вам сообщим")
      await bot.forward_message(chat_id=-1002146003569, from_chat_id=message.chat.id, message_id=message.message_id)
      await bot.send_message(chat_id=-1002146003569, text=f'{students_id[message.from_user.id]}, {message.from_user.username}')
    except BaseException:
      print("error")


async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())