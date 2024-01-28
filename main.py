import telebot
from config import token
from telebot import types
import sqlite3
import requests
import json

bot = telebot.TeleBot(token)
name = None
API = "da204a9bac6691cbd4a21dfd41997f0c"

@bot.message_handler(commands=['help'])
def help(message):
    # открытие соединения с базой данных
    connection = sqlite3.connect('Viral.sql')
    cursor = connection.cursor()

    # Подготовка sql команды
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    # Синхранизация этой команды
    connection.commit()
    # Закрываем соединение с базой данных
    cursor.close()
    connection.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегестрирую! Введите своё имя')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip() # Удалить пробелы стрип
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip() # Удаоить пробелы стрип
    connection = sqlite3.connect('Viral.sql')
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    connection.commit()
    cursor.close()
    connection.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователь', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегестрирован', reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перейти на сайт')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Удалить фото')
    btn3 = types.KeyboardButton('Изменить текст')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "Привет! Я умею делать пару вещей, потыкай кнопки)", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/help')
    markup.row(btn1)
    btn2 = types.KeyboardButton('/start')
    btn3 = types.KeyboardButton('/weather')
    markup.row(btn2, btn3)
    if message.text == "Перейти на сайт":
        bot.send_message(message.chat.id, 'website is open', reply_markup=markup)
    elif message.text == "Удалить фото":
        bot.send_message(message.chat.id, 'delete', reply_markup=markup)
    elif message.text == "Изменить текст":
        bot.send_message(message.chat.id, 'edit', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Привет, Отправь фото на Инлайнов\n "
                                          "Для Создания таблицы введите команду /help\n "
                                          "Чтобы получить погоду введите /weather", reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://yandex.ru')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete') #Параметр при нажатии будет вызываться функция delete
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn2, btn3)
    bot.reply_to(message, "Крутая фотография", reply_markup=markup)


@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Привет, рад теб видеть! Напиши название города')
    bot.register_next_step_handler(message, get_weather)

def get_weather(message):
    city = message.text.strip().lower() #Удаляет пробелы до и после самой строки и lower() привести к нижнему регистру
    try:
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        data = json.loads(res.text)   # метод loads не load
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Сейчас погода: {temp} По Цельсию')

        image = 'sunny.png' if temp > 5.0 else 'sun.png'
        file = open('./'+image, 'rb')
        bot.send_photo(message.chat.id, file)
    except:
        bot.send_message(message.chat.id, f'Произошла ошибка, повторите позже')

#Спец декоратор для кол бек дата
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):  # при удалить фото передастся delete
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'users':
        connection = sqlite3.connect('Viral.sql')
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users")
        users = cursor.fetchall() # Вместо конекта и коммита и спользуем курсор и фетчолл для поиска всего по запросу

        info = ''
        for el in users:
            info += f'Имя: {el[1]}, Пароль: {el[2]}\n' # Так как 0 элемент это id, 1 - name, 2 - password
        cursor.close()
        connection.close()

        bot.send_message(callback.message.chat.id, info)

if __name__ == "__main__":
    bot.infinity_polling()