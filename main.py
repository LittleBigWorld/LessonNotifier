from datetime import *
import telebot
import json
import config
import time


week = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
bot = telebot.TeleBot(config.token)

with open('first_subgroup_schedule.json', encoding="utf-8") as js:
    first_subgroup_data = json.load(js)

with open('second_subgroup_schedule.json', encoding="utf-8") as js:
    second_subgroup_data = json.load(js)

with open('users.json') as js:
    users = json.load(js)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Вітаю {message.from_user.first_name}!\n"
                                      f"Я <b>{bot.get_me().first_name}</b>,"
                                      f" бот який сповіщує студента про початок пари. "
                                      f"\nНапиши /help для перегляду доступних команд.", parse_mode='html')


@bot.message_handler(commands=['help'])
def show_commands(message):
    bot.send_message(message.chat.id, "/start - Початок роботи"
                                      "\n/subgroup1 - Перша підгрупа"
                                      "\n/subgroup2 - Друга підгрупа"
                                      "\n/leave - Вимкнути сповіщення"
                                      "\n/help - Показати доступні команди")


def notify():
    first_subgroup_schedule = first_subgroup_data[week[datetime.now().weekday()]]
    second_subgroup_schedule = second_subgroup_data[week[datetime.now().weekday()]]

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        temp = current_time.split(':')
        forward_time_sec = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2]) + 600
        forward_time = ('%02d:%02d:%02d' % (
            forward_time_sec // 3600, forward_time_sec % 3600 // 60, forward_time_sec % 3600 % 60))

        if current_time == "00:00:00":
            first_subgroup_schedule = first_subgroup_data[week[datetime.now().weekday()]]
            second_subgroup_schedule = second_subgroup_data[week[datetime.now().weekday()]]

        if forward_time in first_subgroup_schedule:
            for i in users["subgroup1"]:
                bot.send_message(i, f'Пара "{first_subgroup_schedule[forward_time]["name"]}" '
                                    f'почнеться через 10 хвилин \nПосилання: '
                                    f'{first_subgroup_schedule[forward_time]["link"]}')

        if forward_time in second_subgroup_schedule:
            for i in users["subgroup2"]:
                bot.send_message(i, f'Пара "{second_subgroup_schedule[forward_time]["name"]}" '
                                    f'почнеться через 10 хвилин \nПосилання: '
                                    f'{second_subgroup_schedule[forward_time]["link"]}')

        if current_time in first_subgroup_schedule:
            for i in users["subgroup1"]:
                bot.send_message(i, f'Пара: "{first_subgroup_schedule[current_time]["name"]}" почалась. '
                                    f'\nПосилання: {first_subgroup_schedule[current_time]["link"]}')

        if current_time in second_subgroup_schedule:
            for i in users["subgroup2"]:
                bot.send_message(i, f'Пара: "{second_subgroup_schedule[current_time]["name"]}" почалась.'
                                    f'\nПосилання: {second_subgroup_schedule[current_time]["link"]}')

        time.sleep(1)


bot.polling(none_stop=True)
