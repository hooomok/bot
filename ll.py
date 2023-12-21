import telebot
import requests
import json
import math

bot = telebot.TeleBot('6895050185:AAFJ8zQOtuhRicOW4Ky7DXGoFktJ-Oe3ptQ')
api = '6816de05260665a558c4ad33bb6d8961'

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! 😍 \nЯ - очень полезный бот, который сможет тебе помочь одеться по погоде! 🌨 \nДля начала работы введи название своего города! 🏙')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric')

    if res.status_code == 200:
        data = json.loads(res.text)
        city = data["name"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        weather_description = data["weather"][0]["main"]

        code = {
            'Clear': 'ясно ☀️',
            'Clouds': 'облачно ☁️',
            'Rain': 'дождь 🌧',
            'Drizzle': 'небольшой дождь 💧',
            'Thunderstorm': 'гроза ⛈',
            'Snow': 'снег 🌨',
            'Mist': 'туман 🌫',
            'Smoke': 'дым 🌫'
        }

        if weather_description in code:
            wd = code[weather_description]
        else:
            wd = 'необычное явление 😯'

        if temp <= -30 or temp >= 30:
            tip = 'Сегодня неблагоприятные погодные усповия! По возможности останьтесь дома! 😶‍🌫'
        elif temp >= 25.0:
            tip = 'Не забудьте воспользоваться солнцезащитным кремом! 🧴'
        elif temp <= 0.0:
            tip = 'Не забудьте надеть шапку и шарф! 🧣'
        else:
            tip = 'Сегодня прекрасная погода! Не забывайте улыбаться! 😁'

        bot.send_message(message.chat.id, f'Погода в городе {city}! 🤩 \nГрадусная мера составляет {temp} °C! 🌡 \nНа улице сейчас {wd}! \nВлажность составляет {humidity}% ! 💧 \nДавление состовляет {math.ceil(pressure/1.333)} мм рт. ст.! 🌑 \nВетер дует со скоростью {wind} м/с! 🌬 \nСовет дня: {tip}')
    else:
        bot.send_message(message.chat.id, 'Вы ввели название несуществующего города! 😔')

bot.polling(none_stop=True)
