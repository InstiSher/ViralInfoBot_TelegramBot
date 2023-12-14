import telebot
from config import token
from telebot import types
import sqlite3

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['help'])
def help(message):
    # открытие соединения с базой данных
    connection = sqlite3.connect('Viral.sql')
    cursor = connection.cursor()

    # Подготовка sql команды
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    # Синхранизация этой команды
    connection.commit()
    # Закрываем соединение с базой данных
    cursor.close()
    connection.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегестрирую! Введите своё имя')
    bot.register_next_step_handler_by_chat_id(message, user_name)


def user_name(message):
    pass

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перейти на сайт')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Удалить фото')
    btn3 = types.KeyboardButton('Изменить текст')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "Привет, Выдай фото на Инлайны", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == "Перейти на сайт":
        bot.send_message(message.chat.id, 'website is open')
    elif message.text == "Удалить фото":
        bot.send_message(message.chat.id, 'delete')
    elif message.text == "Изменить текст":
        bot.send_message(message.chat.id, 'edit')


@bot.message_handler(content_types=['photo'])
def photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://yandex.ru')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete') #Параметр при нажатии будет вызываться функция delete
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn2, btn3)
    bot.reply_to(message, "Крутая фотография", reply_markup=markup)


#Спец декоратор для кол бек дата
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):  # при удалить фото передастся delete
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)



if __name__ == "__main__":
    bot.infinity_polling()