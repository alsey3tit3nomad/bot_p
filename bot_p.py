Token = '123M'

import re
from aiogram import F
import json
import asyncio
from asyncio import sleep
from aiogram.types import message
import pandas as pd
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
bot = Bot(token=Token)
dp = Dispatcher()
# 0 - students_names
# 1 - students_id
price_int = 0
students_names = {}
students_id = {}
op = {}
with open("data.json", encoding="UTF-8") as file_in:
  students_names, students_id, op = json.load(file_in)
print(students_names)
print(students_id)

def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

@dp.message(CommandStart())
async def on_message(message):
    global students_names, students_id, op
    with open("data.json", "w", encoding="UTF-8") as file_out:
      help_js = []
      help_js.append(students_names)
      help_js.append(students_id)
      help_js.append(op)
      json.dump(help_js, file_out, ensure_ascii=False, indent=2)
    await bot.send_message(chat_id=-1002146003569, text=f'@{message.from_user.username} нажал start')
    if message.chat.id != -1002146003569:
        students_id[message.from_user.id] = False
        await message.answer(f'привет, {message.from_user.first_name}.')
        students_id[message.from_user.id] = False
        kb = [
        [
            types.KeyboardButton(text="Я политолог"),
            types.KeyboardButton(text="Я с другой ОП")
        ],
        ]
        keyboard = types.ReplyKeyboardMarkup(
          keyboard=kb,
          resize_keyboard=True,
        )
        await message.answer(f'Продажи билетов для НЕполитологов закрыты.\nЕсли мы не найдем вас среди политогов, то это будет добровольное пожертвование организаторам)))\n\nЕсли ты политолог_иня - welcome!', reply_markup=keyboard)
        await sleep(1)
        try:
            await message.delete()
        except BaseException:
            pass

@dp.message(F.text.lower() == 'я политолог')
async def polit(message):
  global op
  if message.chat.id != -1002146003569:
    await message.answer(f"Чтобы попасть на самое таинственное мероприятие этой весны, нужно всего-то ничего...\n\nУкажите свое полное ФИО, чтобы продолжить процесс {strike('Кафки')} покупки билетов на метаПосвят | похороны политфака.", reply_markup=types.ReplyKeyboardRemove())
    op[message.chat.id] = True
@dp.message(F.text.lower() == 'я с другой оп')
async def no_polit(message):
  global op
  if message.chat.id != -1002146003569:
    await message.answer(f'Сейчас мы принимаешь только политологов', reply_markup=types.ReplyKeyboardRemove())
    op[message.chat.id] = False

@dp.message()
async def handle_FIO(message):
  global students_names, students_id, price_int, op
  print(students_names)
  print(students_id)
  with open("data.json", "w", encoding="UTF-8") as file_out:
    help_js = []
    help_js.append(students_names)
    help_js.append(students_id)
    help_js.append(op)
    json.dump(help_js, file_out, ensure_ascii=False, indent=2)
#   {1206163242: 'абоба абоба', 554377474: 'Холодов Тимур'}
# {'абоба абоба': [1206163242, 'wait'], 'Холодов Тимур': [554377474, 'wait']}
  if (message.document == None and message.photo == None):
    try:
      if (message.chat.id != -1002146003569):
        if(op[message.chat.id] == True):
          pass
    except:
      await message.answer('Сейчас продажи открыты только для политологов')
    else:
        print(message)
        if (str(message.text)[:5] != "/yes_" and str(message.text) != "/result" and str(message.text)[:4] != '/no_' and message.chat.id != -1002146003569 and str(message.text) != '/problem_user' and str(message.text) != '/notification' and str(message.text)[:6] != '/price' ):
          try:
            if (students_id[message.from_user.id] == False):
                pass
          except BaseException:
            await message.answer("Для начала процесса покупки билета пришли мне /start")
          else:
                try:
                    if (students_names[students_id[message.chat.id]][1] == 'wait' and op[message.chat.id] == True):
                        await message.answer("Ожидайте подтверждения оплаты.\n\nОрганизаторы метаПосвята не самые быстрые люди.\nДо конца рабочего дня ваша оплата будет подтверждена и мы вам сообщим")
                    elif (type(students_names[students_id[message.chat.id]][1]) == int and op[message.chat.id] == True):
                        await message.answer('Поздравляем, вы купили билет ! К сожалению, я просто написанный бот на питоне, поэтому пообщаться я с вами не могу, но пообщаться вы сможете\n\nна метаПосвяте | похороны политфака\n16.03.2024')
                    elif (students_names[students_id[message.chat.id]][1] == 'no' and op[message.chat.id] == True):
                        await message.answer('Отправьте чек в виде файла или фотографии')
                except BaseException:
                        pattern1 = r'([a-zA-Zа-яА-ЯёЁ]+)(\s+)([a-zA-Zа-яА-ЯёЁ]+)(\s+)([a-zA-Zа-яА-ЯёЁ]+)'
                        pattern2 = r'[a-zA-Zа-яА-ЯёЁ]+\s+[a-zA-Zа-яА-ЯёЁ]+'
                        my_str = message.text
                        res1 = re.fullmatch(pattern1, my_str)
                        res2 = re.fullmatch(pattern2, my_str)
                        print(not (res1 or res2))
                        if not (res1 or res2):
                            await message.answer('Вы неправильно ввели ФИО: в вашем сообщении есть цифры или недостаточно слов')
                        else:
                            FIO = str(message.text)
                            students_names[FIO] = [message.from_user.id, "no"]
                            students_id[message.from_user.id] = FIO
                            await message.answer(f"Далее перечислите стоимость билета {price_int}р на удобный вам банк:\n\nЕва З.П. — 5536914056119104 — ТИНЬКОФФ\nТимур Х.А. — 2202206721668189 — СБЕР\n\nА затем пришлите либо чек об оплате в формате документа(!) или фотографией(!)")
                            await bot.send_message(chat_id=-1002146003569, text=f'@{message.from_user.username}: ввел ФИО')
        elif (str(message.text)[:5] == "/yes_" and message.chat.id == -1002146003569):
          mes_inf = str(message.text).strip("/yes_")
          mes_inf = mes_inf.split("_")
          name = mes_inf[0]
          n_sum = int(mes_inf[1])
          students_names[name][1] = n_sum
          with open("file.txt", "a") as file:
            file.write(str(name + ";" + str(n_sum)+ "\n"))
          await bot.send_message(chat_id = students_names[name][0], text = "Оплата подтверждена!\nЖдём вас на метаПосвяте | похороны политфака.\n\n16.03.2024")
        elif (str(message.text)[:4] == '/no_' and message.chat.id == -1002146003569):
          mes_inf = str(message.text).strip("/no_")
          name = mes_inf
          print(students_names[name][0])
          await bot.send_message(chat_id = students_names[name][0], text = 'Оплата не прошла.\nПроверьте, точно ли вы скинули именно чек?\nПовторите попытку. В случае, если вы уверены, что действительно оплатили билет, напишите организаторам:\n@timurkholodov')
        elif (str(message.text) == '/problem_user' and message.chat.id == -1002146003569):
            for i in students_id.keys():
                if (len(students_names) != 0):
                    if len(students_names[students_id[i]]) == 2:
                        if type(students_names[students_id[i]][1]) != int:
                            await bot.send_message(chat_id=i, text=f'Вы начали использовать бота, но почему-то до сих пор не купили билет.\n\nЕсли у вас возникли какие-то проблемы и/или вы хотите его купить вручную: пишите @kholodovtimur')
        elif (str(message.text) == '/notification' and message.chat.id == -1002146003569):
            for i in students_id.keys():
                await bot.send_message(chat_id=i, text=f'метаПосвят | похороны политфака уже совсем скоро!\n\nнапоминаем вам о том, что пройдёт он 16 марта по адресу: улица Самокатная д.4 стр 19.\n\nждём вас, если вы уже купили билеты и ждём вашей покупки билетов, если у вас их еще нет!')
        elif (str(message.text)[:6] == '/price' and message.chat.id == -1002146003569):
          mes_inf = str(message.text).strip("/price_")
          price_int = int(mes_inf)
          print(price_int)
          print(type(price_int))
        else:
          if message.chat.id == -1002146003569:
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
  global students_names, students_id, op
  with open("data.json", "w", encoding="UTF-8") as file_out:
    help_js = []
    help_js.append(students_names)
    help_js.append(students_id)
    help_js.append(op)
    json.dump(help_js, file_out, ensure_ascii=False, indent=2)
  print(students_names)
  print(students_id)
  print(op)
  if (message.document == None or message.photo == None):
    try:
      students_names[students_id[message.from_user.id]][1] = "wait"
      await message.answer("Ожидайте подтверждения оплаты.\n\nОрганизаторы метаПосвята не самые быстрые люди.\nДо конца рабочего дня ваша оплата будет подтверждена и мы вам сообщим")
      await bot.forward_message(chat_id=-1002146003569, from_chat_id=message.chat.id, message_id=message.message_id)
      await bot.send_message(chat_id=-1002146003569, text=f'{students_id[message.from_user.id]}')
    except BaseException:
      print("error")


async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
