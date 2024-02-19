'''
from pycbrf.toolbox import ExchangeRates # импортируем библиотеку

rates = ExchangeRates('2024-02-18') # задаем дату, за которую хотим получить данные
#ExchangeRate(id='R01815', name='Вон Республики Корея', code='KRW', num='410', value=Decimal('69.3045'), par=Decimal('1000'), rate=Decimal('0.0693045'))
result = rates['KRW']
if result.par == 1:
    print(f'{result.par} Рубль равен {result.value}')
else:
    print(f'{result.par} Рублей равно {result.value} {result.name}')

print(rates)
'''

import telebot
from telebot import types
from config import token
from currency_converter import CurrencyConverter
currency = CurrencyConverter()
amount = 0

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат, введите сумму')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("RUB/KRW", callback_data='rub/krw')
        btn2 = types.InlineKeyboardButton("RUB/USD", callback_data='rub/usd')
        btn3 = types.InlineKeyboardButton("EUR/USD", callback_data='eur/usd')
        btn4 = types.InlineKeyboardButton("RUB/EUR", callback_data='rub/eur')
        btn5 = types.InlineKeyboardButton("Другое значение", callback_data='else')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)

    else:
        bot.send_message(message.chat.id, 'Введите число больше нуля')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново ввести сумму')
        bot.register_next_step_handler(call.message, summa)

    else:
        bot.send_message(call.message.chat.id, 'Введите пару значение через слеш, например "kzt/usd"')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново ввести сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так, введите пару значений заново')
        bot.register_next_step_handler(message, my_currency)

if __name__ == "__main__":
    bot.infinity_polling()