import datetime  # для отслеживания всех данных в реальном времени

import COVID19Py  # для работы с информацией о COVID-19

import requests  # для работы с API погоды

import telebot  # для работы с ботом

from pycbrf.toolbox import ExchangeRates  # для работы с базой данных Центробанка

# токен
bot = telebot.TeleBot('1125432380:AAE5heK6G69ZM6Dz2nmBrpBpHjL0G0Is63E')
# дата
today = datetime.datetime.today()
datenow = today.strftime("%Y-%m-%d-%H.%M.%S")[0:-9]
# список валют по сегодняшней дате
rates = ExchangeRates(datenow)
# ключ доступа к сервису OpenWeatherMap
api_key = "29b80b85e54d33543a13a5962a8185cb"
# для отправки запросв погоды
base_url = "http://api.openweathermap.org/data/2.5/weather?"

covid19 = COVID19Py.COVID19()


# начало работы
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Здравствуй.')

    bot.send_message(message.chat.id, "Напиши мне /help, чтобы узнать, что я могу сделать!")


# описание возможностей
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Я могу узнать курс пяти самых торгуемых "
                                      "валют(доллар, евро, иена, фунт и австралийский доллар) к рублю,"
                                      " вывести текущую погоду в любой точке мира, "
                                      "а также вывести статистику по коронавирусу для некоторых стран СНГ, "
                                      " США и Китая")

    bot.send_message(message.chat.id, "Для того, чтобы узнать курс валюты, просто напишите ее название(например, евро)"
                                      " и я выведу ее курс к рублю, основываясь на данных ЦБ РФ. Чтобы узнать погоду"
                                      " в той или иной точке мира, напиши мне "
                                      "'погода (название города в именительном падеже)', я сразу же напишу, какая"
                                      " там сейчас температура, давление, влажность."
                                      " Чтобы узнать статистику по коронавирусу напиши мне "
                                      "'коронавирус (а тут название страны, это может быть Россия,"
                                      " США, Китай, Казахстан, Украина, Беларусь)', чтобы узнать статистику по "
                                      "всему миру, не нужно указывать название страны."
                                      "Приятной работы!")


# работа с сообщениями пользователя
@bot.message_handler(content_types=['text'])
def send_text(message):
    # ВАЛЮТЫ

    # доллар
    if message.text.lower() == 'доллар' or message.text.lower() == 'доллар сша':
        bot.send_message(message.chat.id, f"Один доллар США сейчас стоит {str(rates['USD'][4])} руб.")

    # евро
    if message.text.lower() == 'евро':
        bot.send_message(message.chat.id, f"Один евро стоит {str(rates['EUR'][4])} руб.")

    # иена
    if message.text.lower() == 'японская иена' or message.text.lower() == "иена":
        bot.send_message(message.chat.id, f"Одна японская иена стоит {str(rates['JPY'][4])} руб.")

    # фунт
    if message.text.lower() == 'британский фунт стерлингов' or message.text.lower() == 'фунт' or \
            message.text.lower() == 'фунт стерлингов':
        bot.send_message(message.chat.id, f"Один фунт стерлингов Соединенного Королевства стоит "
                                            f"{str(rates['GBP'][4])} руб.")

    # австралийский доллар
    if message.text.lower() == 'австралийский доллар':
        bot.send_message(message.chat.id, f"Один доллар Австралии стоит {str(rates['AUD'][4])} руб.")


    #------------------
    # ПОГОДА
    if "погода" in message.text.lower():
        city_name = ' '.join(message.text.lower().split()[1:])
        response = requests.get(base_url + "appid=" + api_key + "&q=" + city_name)
        # json метод объекта ответа
        # преобразовать данные формата json в
        # данные формата питона
        x = response.json()
        # Теперь x содержит список вложенных словарей

        if x["cod"] != "404":
            # сохранить значение "main"
            # введите переменную y
            y = x["main"]
            # сохранить значение, соответствующее
            # к "временному" ключу y
            current_temperature = y["temp"] - 273.15
            # вычитаем 273.15, чтобы перевести из кельвинов в цельсии
            # сохранить значение, соответствующее
            # к клавише "давления" у
            current_pressure = y["pressure"]
            # сохранить значение, соответствующее
            # к клавише «влажность» у
            current_humidiy = y["humidity"]
            # сохранить значение «погода»
            # введите переменную z
            z = x["weather"]
            # сохранить значение, соответствующее
            # к ключу "описание" в
            # 0 индекс z

            weather_description = z[0]["description"]


        bot.send_message(message.chat.id,
                         f"Температура: {str(int(current_temperature))} градусов по Цельсию, давление(hPa): "
     
                         f"{str(current_pressure)}, влажность(%): {str(current_humidiy)}, {weather_description} ")


    # --------------
    # КОРОНАВИРУС
    if "коронавирус" in message.text.lower():
        final_message = ''
        if "россия" in message.text.lower() or "рф" in message.text.lower():
            location = covid19.getLocationByCountryCode("RU")
        elif "сша" in message.text.lower():
            location = covid19.getLocationByCountryCode("US")
        elif "украина" in message.text.lower():
            location = covid19.getLocationByCountryCode("UA")
        elif "беларусь" in message.text.lower():
            location = covid19.getLocationByCountryCode("BY")
        elif "казахстан" in message.text.lower():
            location = covid19.getLocationByCountryCode("KZ")
        elif "китай" in message.text.lower():
            location = covid19.getLocationByCountryCode("CH")

        else:  # для всего мира
            location = covid19.getLatest()
            final_message = f"<u>Данные по всему миру:</u>\n<b>Заболевших: </b>{location['confirmed']:,}\n<b>Смертей: </b>{location['deaths']:,}"

        # для отдельной страны
        if final_message == "":
            date = location[0]['last_updated'].split("T")
            time = date[1].split(".")

            final_message = f"<u>Данные по стране:</u>\nНаселение: {location[0]['country_population']:,}\n" \
                f"Последнее обновление: {date[0]} {time[0]}\nПоследние данные:\n<b>" \
                f"Заболевших: </b>{location[0]['latest']['confirmed']:,}\n<b>Смертей: </b>" \
                f"{location[0]['latest']['deaths']:,}"

        bot.send_message(message.chat.id, final_message, parse_mode="html")


bot.polling()
