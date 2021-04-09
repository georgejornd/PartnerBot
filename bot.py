# coding: utf8
import telebot
from telebot import apihelper
from telebot import types
import os
import requests
import json
import sqlite3

bot = telebot.TeleBot("четыре")

dir_file = os.getcwd()

pay_users_numb = []

pay_users_sum = {}

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_id = str(message.from_user.id)

    if user_id in pay_users_numb:
        keyboard = types.InlineKeyboardMarkup()
        key_glav = types.InlineKeyboardButton(text='Назад', callback_data='main_page')
        keyboard.add(key_glav)
        bot.send_message(message.chat.id, text='Введите сумму', reply_markup=keyboard)
        pay_users_numb.remove(user_id)
        pay_users_sum[user_id] = message.text

    elif user_id in pay_users_sum:
        keyboard = types.InlineKeyboardMarkup()
        key_glav = types.InlineKeyboardButton(text='Назад', callback_data='main_page')
        keyboard.add(key_glav)
        if message.text.isdigit(): 
            os.chdir(dir_file + '\\users\\' + str(user_id))
            user_balance = open('balance.txt')
            u_bal = user_balance.read()
            if int(message.text) <= float(u_bal):
                if int(message.text) != 0:
                    balance = float(u_bal)
                    user_balance.close()
                    user_balance = open('balance.txt', 'w')
                    user_balance.write(str(balance-int(message.text)))
                    user_balance.close()
                    os.chdir(dir_file)
                    list_vipl = open('Список выплат.txt', 'a')
                    list_vipl.write(user_id + ' - ' + message.text + ' рублей\n')
                    list_vipl.close()
                    keyboard = types.InlineKeyboardMarkup()
                    key_glav = types.InlineKeyboardButton(text='Вернуться', callback_data='main_page')
                    keyboard.add(key_glav)
                    bot.send_message(message.chat.id, 'Ожидайте, мы проверим и обработаем вашу заявку на вывод', reply_markup=keyboard)
                else:
                    bot.send_message(message.chat.id, 'Сумма должна быть больше нуля', reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, 'Сумма превышает баланс', reply_markup=keyboard)
            user_balance.close()
            

        else:
            bot.send_message(message.chat.id, 'Сумма должна быть целым числом', reply_markup=keyboard)
    os.chdir(dir_file)
    
    if message.text.split()[0] == '/start':
        os.chdir(dir_file + '\\users')
        if os.path.isdir(dir_file + '\\users\\' + str(user_id)):
            bot.send_message(message.chat.id, 'Вы уже зарегистрированы')
        else:
            bot.send_message(message.chat.id, 'Вы зарегистрировались')

            os.mkdir(dir_file + '\\users\\' + str(user_id))
            
            os.chdir(dir_file + '\\users\\' + str(user_id))

            user_balance = open('balance.txt', 'w')
            user_balance.write('0')
            user_balance.close()

            user_ref_1 = open('ref_1.txt', 'w')
            user_ref_1.close()

            user_ref_2 = open('ref_2.txt', 'w')
            user_ref_2.close()

            user_ref_3 = open('ref_3.txt', 'w')
            user_ref_3.close()

            user_ref_4 = open('ref_4.txt', 'w')
            user_ref_4.close()

            user_ref_5 = open('ref_5.txt', 'w')
            user_ref_5.close()

            user_ref_6 = open('ref_6.txt', 'w')
            user_ref_6.close()

            user_ref_7 = open('ref_7.txt', 'w')
            user_ref_7.close()
                    
            if len(message.text.split()) > 1:    
                os.chdir(dir_file + '\\ref')
                if os.path.isfile(dir_file + '\\ref\\' + message.text.split()[1] + '.txt'):
                    bot.send_message(message.chat.id, 'Вас пригласил ' + message.text.split()[1])
                    os.chdir(dir_file + '\\users\\' + str(user_id))
                    user_file = open('ref_to.txt', 'w')
                    user_file.write(message.text.split()[1])
                    user_file.close()
                    os.chdir(dir_file + '\\users\\' + message.text.split()[1])
                    ref_1 = open('ref_1.txt', 'a')
                    ref_1.write(user_id + '\n')
                    ref_1.close()
                    i = 0
                    while i < 7:
                        if os.path.isfile(dir_file + '\\users\\' + message.text.split()[1] + '\\' + 'ref_to.txt'):
                            ref = open('ref_to.txt')
                            os.chdir(dir_file + '\\users\\' + ref.read())
                            ref.close()
                            ref = open('ref_' + str(i + 2) + '.txt', 'a')
                            ref.write(user_id)
                            ref.close()
                            i += 1
                        else:
                            i = 7
                                            
                else:
                    bot.send_message(message.chat.id, 'Реферальная ссылка не найдена')
                
        os.chdir(dir_file)
        main_page(message)
    

	
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user_id = str(call.from_user.id)

    if call.data == 'main_page':
        if user_id in pay_users_numb:
            pay_users_numb.remove(user_id)
        if user_id in pay_users_sum:
            pay_users_sum.pop(user_id)
        main_page(call.message)
    
    if call.data == 'glav':
        keyboard = types.InlineKeyboardMarkup()
        key_glav = types.InlineKeyboardButton(text='Вернуться', callback_data='main_page')
        keyboard.add(key_glav)
        
        glav_file = open('Главная.txt', encoding='utf-8')
        bot.send_message(call.message.chat.id, glav_file.read(), reply_markup=keyboard)
        glav_file.close()

    if call.data == 'cab':
        os.chdir(dir_file + '\\users\\' + str(user_id))

        keyboard = types.InlineKeyboardMarkup()
        key_viv = types.InlineKeyboardButton(text='Вывести средства', callback_data='viv')
        keyboard.add(key_viv)
        key_glav = types.InlineKeyboardButton(text='Вернуться', callback_data='main_page')
        keyboard.add(key_glav)

        user_balance = open('balance.txt')
        user_ref_1 = open('ref_1.txt')
        user_ref_2 = open('ref_2.txt')
        user_ref_3 = open('ref_3.txt')
        user_ref_4 = open('ref_4.txt')
        user_ref_5 = open('ref_5.txt')
        user_ref_6 = open('ref_6.txt')
        user_ref_7 = open('ref_7.txt')
        
        bot.send_message(call.message.chat.id, 'Ваш баланс: ' + user_balance.read() + ' рублей' +
                         '\nРефералов 1 уровня: ' + str(len(user_ref_1.readlines())) +
                         '\nРефералов 2 уровня: ' + str(len(user_ref_2.readlines())) +
                         '\nРефералов 3 уровня: ' + str(len(user_ref_3.readlines())) +
                         '\nРефералов 4 уровня: ' + str(len(user_ref_4.readlines())) +
                         '\nРефералов 5 уровня: ' + str(len(user_ref_5.readlines())) +
                         '\nРефералов 6 уровня: ' + str(len(user_ref_6.readlines())) +
                         '\nРефералов 7 уровня: ' + str(len(user_ref_7.readlines())),
                         reply_markup=keyboard)
        
        user_balance.close()
        user_ref_1.close()
        user_ref_2.close()
        user_ref_3.close()
        user_ref_4.close()
        user_ref_5.close()
        user_ref_6.close()
        user_ref_7.close()
        
        os.chdir(dir_file)

    if call.data == 'podp':
        os.chdir(dir_file)
        sum_opl = open('Сумма оплаты.txt')
        qiwi_number = open('Номер QIWI.txt')
        
        keyboard = types.InlineKeyboardMarkup()
        
        key_check = types.InlineKeyboardButton(text='Проверить оплату', callback_data='check')
        keyboard.add(key_check)
        
        key_glav = types.InlineKeyboardButton(text='Назад', callback_data='main_page')
        keyboard.add(key_glav)
        
        bot.send_message(call.message.chat.id, text='Стоимость подписки: ' + sum_opl.read() + ' рублей\nПришлите их на QIWI ' + qiwi_number.read() + ' и в коментарий укажите код ' + user_id, reply_markup=keyboard)
        
        qiwi_number.close()
        sum_opl.close()

    if call.data == 'viv':
        pay_users_numb.append(user_id)
        bot.send_message(call.message.chat.id, text='Введите ваш номер QIWI')

    if call.data == 'check':
        if not os.path.isfile(dir_file + '\\users\\' + str(user_id) + '\\' + 'ref.txt'):
            fp = open('Номер QIWI.txt')
            ft = open('Токен QIWI.txt')
            sumo = open('Сумма оплаты.txt')
            bot.send_message(call.message.chat.id, text='Ваш платеж обрабатывается')
        
            QIWI_TOKEN = ft.read()
            QIWI_ACCOUNT = fp.read()
        
            s = requests.Session()
            s.headers['authorization'] = 'Bearer ' + QIWI_TOKEN  
            parameters = {'rows': '50'}
            h = s.get('https://edge.qiwi.com/payment-history/v1/persons/'+ QIWI_ACCOUNT +'/payments', params = parameters)
            req = json.loads(h.text)
            summ = int(sumo.read())

            for i in range(len(req['data'])):
                if str(req['data'][i]['comment']) == user_id:
                    if req['data'][i]['sum']['amount'] == summ:
                        os.chdir(dir_file + '\\ref\\')

                        ref_file = open(user_id + '.txt', 'w')
                        ref_file.write(user_id)
                        ref_file.close()

                        keyboard = types.InlineKeyboardMarkup()
                        key_glav = types.InlineKeyboardButton(text='Назад', callback_data='main_page')
                        keyboard.add(key_glav)
    
                        bot.send_message(call.message.chat.id, text='Ваша реферальная ссылка -\nhttps://t.me/PartnerProgramBot?start=' + user_id, reply_markup=keyboard)                

                        os.chdir(dir_file)
                    
                        money_ref_file = open('Деньги за рефералов.txt')
                        money_ref = money_ref_file.readlines()
                        money_ref_file.close()

                        os.chdir(dir_file + '\\users\\' + str(user_id))

                        ref_user = open('ref.txt', 'w')
                        ref_user.close()
        
                        if os.path.isfile(dir_file + '\\users\\' + user_id + '\\' + 'ref_to.txt'):
                            os.chdir(dir_file + '\\users\\' + user_id)
                            ref_txt = open('ref_to.txt')
                            ref_id = ref_txt.read()
                            ref_txt.close()
                        
                            i = 0
                            while i < 7:
                                os.chdir(dir_file + '\\users\\' + ref_id)
                                ref_bal_file = open('balance.txt')
                                ref_bal = float(ref_bal_file.read())
                                ref_bal_file.close()
                                ref_bal += float(money_ref[i])
                                ref_bal_file = open('balance.txt', 'w')
                                ref_bal_file.write(str(ref_bal))
                                ref_bal_file.close()
                                if os.path.isfile(dir_file + '\\users\\' + ref_id + '\\' + 'ref_to.txt'):
                                    ref_txt = open('ref_to.txt')
                                    ref_id = ref_txt.read()
                                    ref_txt.close()
                                    i += 1
                                else:
                                    i = 7
                    
                        os.chdir(dir_file)
                    
            sumo.close()
            ft.close()
            fp.close()
    elif call.data == 'check':
        keyboard = types.InlineKeyboardMarkup()
        key_glav = types.InlineKeyboardButton(text='Назад', callback_data='main_page')
        keyboard.add(key_glav)
        bot.send_message(message.chat.id, text='Ваша реферальная ссылка -\nhttps://t.me/PartnerProgramBot?start=' + user_id, reply_markup=keyboard)
        

def main_page(message):
    keyboard = types.InlineKeyboardMarkup()
    
    key_glav = types.InlineKeyboardButton(text='Главная', callback_data='glav')
    keyboard.add(key_glav)

    key_cab = types.InlineKeyboardButton(text='Кабинет', callback_data='cab')
    keyboard.add(key_cab)

    key_podp = types.InlineKeyboardButton(text='Подписка', callback_data='podp')
    keyboard.add(key_podp)

    bot.send_message(message.chat.id, text='Выбери действие.', reply_markup=keyboard)
bot.polling()
