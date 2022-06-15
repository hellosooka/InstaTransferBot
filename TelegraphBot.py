import instaloader
import telebot
import os
import glob
from time import sleep
import shutil


#Бот Телеграмма
bot = telebot.TeleBot('5235940973:AAGGvzSKGln7b7vO77s4XafiZJJxnV2pS8E')



#Бот Инстаграмма
instaBot = instaloader.Instaloader()

user_dict = {}


class User:
    login = None
    password = None
        

#Вступление
@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text == '/start':
        bot.send_message(message.chat.id,"Привет! Я простой и быстрый инструмент переноса постов из Instagram в Telegram. \nДля моей корректной работы ты должен знать пароль и логин аккаунта из которого хочешь взять фотографии. Без него инстаграм не позволит нам это сделать. \nНе беспокойся, твои данные остаются только здесь, мы их не собираем. \n\nЧтобы начать тыкни /newuser")
    elif message.text == '/newuser':
        bot.send_message(message.chat.id, "Название инстаграм аккаунта:")
        bot.register_next_step_handler(message, addLogin)
    else:
        bot.send_message(message.chat.id,"Я не отвечаю на сообщения. \nЕсли хочешь скачать фотографии тыкни /newuser")


#Добавление имени
def addLogin(message):
    user = User()
    user.login = message.text
    user_dict[message.chat.id] = user
    
    bot.send_message(message.from_user.id, 'Пароль:')
    bot.register_next_step_handler(message, addPassword)


#Добавление пароля
def addPassword(message):
    global password

    user = user_dict[message.chat.id]
    user.password = message.text

    try:

        instaBot.login(user.login, user.password)
        bot.send_message(message.from_user.id, 'Упаковываем файлы.\nЯ тебе отправлю все что найду. \nНа обработку всех фотографий и файлов уходит от 5 минут до 1 дня. Сильно зависит от колличества фотографий и пользователей')
        instaBot.download_profile(user.login)

        path = str(user.login)
        photo = glob.glob(path + '/' + "*.*")

        
        for photo in photo:
            sleep(1)
            bot.send_document(message.chat.id, open(photo, 'rb'))
        shutil.rmtree(path)

        bot.send_message(message.from_user.id, 'Выгрузка завершена \nЧтобы еще раз мной воспользоваться: /newuser')
    except BaseException:
        bot.send_message(message.from_user.id, "Неправильно введены данные, попробуйте еще раз /newuser")

    

    
    




    
    


bot.infinity_polling()
    


    
        






