# -*- coding: utf-8 -*-

import json
from telegram.ext import (Updater, CommandHandler, Filters, MessageHandler, ConversationHandler)

title_to_be_remove = ""
title_to_be_edit = ""

users = [USERS ID]


def check_data_validation(data):
    if len(data.split('\n')) == 2:
        try:
            float(data.split('\n')[1])
            return True
        except:
            return False
    else:
        return False


def get_data():
    data = ""
    file = open('data.json', 'r')
    lines = file.readlines()
    for i in range(0, len(lines)):
        data += str(i + 1) + '- ' + json.loads(lines[i])['name'] + '\n' + str(i + 1) + '- ' + str(
            json.loads(lines[i])['price']) + '\n-----\n' if i + 1 != len(lines) else str(i + 1) + '- ' + \
                                                                                     json.loads(lines[i])[
                                                                                         'name'] + '\n' + str(
            i + 1) + '- ' + str(json.loads(lines[i])['price']) + '\n'

    return data


def start(bot, update):
    if update.message.from_user.id in users:
        bot.send_message(
            text=' سلام بهزاد به ربات دیوار خوش آمدی.'.format(
                update.message.from_user.first_name),
            chat_id=update.message.chat_id)


def add_to_file(text):
    file = open('data.json', 'a')
    title = str(text.split('\n')[0].strip())
    price = float(text.split('\n')[1])
    data = {}
    data['name'] = title
    data['price'] = price
    with open('data.json', 'r') as f:
        f = f.readlines()
    if len(f) == 0:
        file.write(json.dumps(data))
    else:
        file.write('\n' + json.dumps(data))
    file.close()


def add_data(bot, update):
    if 'cancel' not in update.message.text.lower():
        if check_data_validation(update.message.text):
            add_to_file(update.message.text)
            bot.send_message(text="اطلاعات با موفقیت ثبت گردید.", chat_id=update.message.chat_id,
                             reply_to_message_id=update.message.message_id)
            return ConversationHandler.END
        else:
            bot.send_message(text="داده های ارسالی طبق فرمت گفته شده نمی‌باشند. پس از اصلاح دوباره ارسال کنید.",
                             chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id)
            return 1
    else:
        bot.send_message(text="عملیات لغو شد.", chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return ConversationHandler.END


def add(bot, update):
    if update.message.from_user.id in users:
        text = '    به منظور اضافه کردن اطلاعات، اطلاعات جدید را در قالب زیر در دو خط ارسال نمایید:\ntitle\nprice\nبه عنوان مثال:\ngalaxy s7\n5400000\nنکته: حروف کوچک و بزرگ در جست و جو تاثیری ندارد.\n  '
        bot.send_message(text=text, chat_id=update.message.chat_id)
        return 1


def add_to_black_list(bot, update):
    if update.message.from_user.id in users:
        text = 'به منظور اضافه کردن اطلاعات به لیست سیاه، اطلاعات را در یک خط ارسال نمایید:'
        bot.send_message(text=text, chat_id=update.message.chat_id)
        return 1


def add_to_black_list_file(text):
    file = open('black_list.txt', 'a')
    title = str(text.split('\n')[0].strip())
    with open('black_list.txt', 'r') as f:
        f = f.readlines()
    if len(f) == 0:
        file.write(title)
    else:
        file.write('\n' + text)
    file.close()


def add_data_to_black_list(bot, update):
    if 'cancel' not in update.message.text.lower():
        add_to_black_list_file(update.message.text)
        bot.send_message(text="اطلاعات با موفقیت در لیست سیاه ثبت گردید.", chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return ConversationHandler.END
    else:
        bot.send_message(text="عملیات لغو شد.", chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return ConversationHandler.END


def show(bot, update):
    if update.message.from_user.id in users:
        bot.send_message(text="داده‌های فعلی به شرح زیر می‌باشند:\n" + get_data(),
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)


def change_city(bot, update):
    if update.message.from_user.id in users:
        with open('current_city.txt', 'r') as file:
            city = file.readlines()
        temp = city[0].replace('\n', '')
        city[0] = city[1] + '\n'
        city[1] = temp
        with open('current_city.txt', 'w') as file:
            file.writelines(city)
        bot.send_message(text="شهر تعویض شد، شهر فعلی: " + city[0],
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)


def show_current_city(bot, update):
    if update.message.from_user.id in users:
        with open('current_city.txt', 'r') as file:
            city = file.readlines()
        bot.send_message(text="شهر فعلی: " + city[0],
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)


def edit(bot, update):
    if update.message.from_user.id in users:
        bot.send_message(text="برای ویرایش اطلاعات وارد شده، عنوانی که می‌خواهید ویرایش شود را وارد کنید:",
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return 1


def edit_data(bot, update):
    if 'cancel' not in update.message.text.lower():
        global title_to_be_edit
        title_to_be_edit = update.message.text
        pre_text = "اطلاعات یافت شده به شرح زیر می‌باشد:\n"
        data = ""
        file = open('data.json', 'r')
        lines = file.readlines()
        for i in range(0, len(lines)):
            if update.message.text.lower() == json.loads(lines[i])['name'].lower():
                data += str(i) + '. ' + json.loads(lines[i])['name'] + '\n' + str(i) + '. ' + str(
                    json.loads(lines[i])['price']) + '\n\n'
                break
        if data == "":
            bot.send_message(text="نتیجه‌ای یافت نشد.",
                             chat_id=update.message.chat_id,
                             reply_to_message_id=update.message.message_id)
            return 1
        else:
            text = "اطلاعات جدید را در غالب دو خط به‌صورت زیر ارسال نمایید:\ntitle\nprice\nبه عنوان مثال:\ngalaxay s7\n5400000"
            bot.send_message(text=pre_text + data + text,
                             chat_id=update.message.chat_id,
                             reply_to_message_id=update.message.message_id)
            return 2
    else:
        bot.send_message(text='عملیات لغو شد.',
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return ConversationHandler.END


def edit_from_file(bot, update):
    if check_data_validation(update.message.text):
        with open('data.json', 'r') as file:
            lines = file.readlines()
        new_data = [data for data in lines if json.loads(data)['name'].lower() != title_to_be_edit.lower()]
        new_data.append('\n')
        new_data.append(
            json.dumps({"name": update.message.text.split('\n')[0], "price": update.message.text.split('\n')[1]}))
        with open('data.json', 'w') as file:
            file.writelines(new_data)
        bot.send_message(text="داده باموفقیت ویرایش شد.",
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return ConversationHandler.END
    else:
        bot.send_message(text="داده های ارسالی طبق فرمت گفته شده نمی‌باشند. پس از اصلاح دوباره ارسال کنید.",
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return 2


def remove_from_file(bot, update):
    global title_to_be_remove
    if int(update.message.text) == 1:
        with open('data.json', 'r') as file:
            lines = file.readlines()
        new_data = [data for data in lines if json.loads(data)['name'].lower() != title_to_be_remove.lower()]
        with open('data.json', 'w') as file:
            file.writelines(new_data)
        bot.send_message(text="با موفقیت پاک شد.",
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return ConversationHandler.END
    else:
        bot.send_message(text="عملیات لغو شد.",
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return ConversationHandler.END


def remove(bot, update):
    if update.message.from_user.id in users:
        bot.send_message(text='به‌منظور حذف داده عنوان را وارد کنید:',
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return 1


def remove_data(bot, update):
    if 'cancel' not in update.message.text.lower():
        global title_to_be_remove
        title_to_be_remove = update.message.text
        text = ''
        verify = 'داده‌ی زیر پس از تایید حذف می‌شود. با ارسال 1 حذف را تایید کنید: (لغو با ارسال cancel)\n\n'
        file = open('data.json', 'r')
        lines = file.readlines()

        for i in range(0, len(lines)):
            if update.message.text.lower() == json.loads(lines[i])['name'].lower():
                text = str(i) + '- ' + json.loads(lines[i])['name'] + '\n' + str(i) + '- ' + str(
                    json.loads(lines[i])['price']) + '\n\n'
                break
        if '' == text:
            bot.send_message(text='عنوان ارسالی شما در داده ها وجود ندارد.',
                             chat_id=update.message.chat_id,
                             reply_to_message_id=update.message.message_id)
            return 1
        else:
            bot.send_message(text=verify + text,
                             chat_id=update.message.chat_id,
                             reply_to_message_id=update.message.message_id)
            return 2
    else:
        bot.send_message(text='عملیات لغو شد.',
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return ConversationHandler.END


def removeAll_data_from_file():
    with open('data.json', 'w') as file:
        file.write('')


def removeAll_data(bot, update):
    if str(update.message.text) == '1':
        removeAll_data_from_file()
        bot.send_message(text="داده‌ها با موفقیت پاک شدند.",
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return ConversationHandler.END
    elif str(update.message.text) == '2':
        bot.send_message(text="عملیات لغو شد.",
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return ConversationHandler.END
    else:
        bot.send_message(text="فقط یکی از دو گزینه‌ی 1-تایید یا 2-لغو را می‌توانید ارسال کنید.",
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return 1


def removeAll(bot, update):
    if update.message.from_user.id in users:
        bot.send_message(text='حذف همه‌ی داده‌ها را تایید می‌کنید؟\n1-تایید\n2-لغو',
                         chat_id=update.message.chat_id,
                         reply_to_message_id=update.message.message_id)
        return 1


def help(bot, update):
    if update.message.from_user.id in users:
        text = "راهنمای استفاده از ربات:\n۱- حروف کوچک و بزرگ در جست و جو تاثیری ندارد پس نگران آن ها نباشید.\n۲- با توجه به اینکه قیمت‌ها در دیوار به تومان می‌باشد قیمت‌های وارد شده توسط شما هم می‌بایست به تومان باشد.\n"
        bot.send_message(text=text, chat_id=update.message.chat_id)


def cancel_handler(bot, update):
    bot.send_message(text='روند کنسل شد برای شروع یکی از دستورات را ارسال نمایید.',
                     chat_id=update.message.chat_id,
                     reply_to_message_id=update.message.message_id)
    return ConversationHandler.END


def alert_message(bot, update):
    bot.send_message(text='دستور نامعتبر!',
                     chat_id=update.message.chat_id,
                     reply_to_message_id=update.message.message_id)


update = Updater('TOKEN', use_context=False)

addHandler = ConversationHandler(
    entry_points=[
        CommandHandler('add', add)],
    states={
        1: [MessageHandler(Filters.text, add_data)]
    },
    fallbacks=[CommandHandler('cancel', cancel_handler)])

blackListHandler = ConversationHandler(
    entry_points=[
        CommandHandler('add_to_black_list', add_to_black_list)],
    states={
        1: [MessageHandler(Filters.text, add_data_to_black_list)]
    },
    fallbacks=[CommandHandler('cancel', cancel_handler)])

removeHandler = ConversationHandler(
    entry_points=[
        CommandHandler('remove', remove)],
    states={
        1: [MessageHandler(Filters.text, remove_data)],
        2: [MessageHandler(Filters.text, remove_from_file)]
    },
    fallbacks=[CommandHandler('Cancel', cancel_handler)])

editHandler = ConversationHandler(
    entry_points=[
        CommandHandler('edit', edit)],
    states={
        1: [MessageHandler(Filters.text, edit_data)],
        2: [MessageHandler(Filters.text, edit_from_file)]
    },
    fallbacks=[CommandHandler('Cancel', cancel_handler)])

removeAllHandler = ConversationHandler(
    entry_points=[
        CommandHandler('remove_all', removeAll)],
    states={
        1: [MessageHandler(Filters.text, removeAll_data)]
    },
    fallbacks=[CommandHandler('Cancel', cancel_handler)])

update.dispatcher.add_handler(CommandHandler('start', start))
update.dispatcher.add_handler(CommandHandler('show', show))
update.dispatcher.add_handler(CommandHandler('change_city', change_city))
update.dispatcher.add_handler(CommandHandler('current_city', show_current_city))
update.dispatcher.add_handler(CommandHandler('help', help))
update.dispatcher.add_handler(addHandler)
update.dispatcher.add_handler(editHandler)
update.dispatcher.add_handler(blackListHandler)
update.dispatcher.add_handler(removeHandler)
update.dispatcher.add_handler(removeAllHandler)
update.dispatcher.add_handler(MessageHandler(Filters.text, alert_message))
update.start_polling()
update.idle()

