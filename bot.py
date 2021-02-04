import telebot
import config
import info


CURRENCY = ('USD', 'EUR', 'RUB')

bot = telebot.TeleBot(config.TOKEN)
information = info.CityInfo()  # интерфейс взаимодействия с различными API


def check_currency(query):
    """Функция, которая возвращает True, если на кнопку из списка CURRENCY нажали"""
    for currency in CURRENCY:
        if currency in query.data:
            return True
    return False


def check_weather(query):
    if query.data == "weather":
        return True
    return False


def check_exchange(query):
    if query.data == "exchange":
        return True
    return False


@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Weather', callback_data='weather'),
                telebot.types.InlineKeyboardButton('Currency Exchange', callback_data='exchange'),
                )
    bot.send_message(chat_id=message.chat.id,
                     text="Hi! You can use the /exchange and /weather functions. New ones will be added soon!",
                     reply_markup=keyboard
                     )


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(
        'Message the developer', url='https://telegram.me/jkban4e'
    ))
    bot.send_message(chat_id=message.chat.id, text='The /exchange functions are now available. New ones will be added soon!',
                     reply_markup=keyboard
                     )


@bot.message_handler(commands=['weather'])
def weather_command(message):
    bot.send_message(chat_id=message.chat.id, text=f"{message.text}")


@bot.callback_query_handler(func=check_weather)
def weather_command_from_start(query):
    bot.send_message(chat_id=query.message.chat.id, text=f"фывафывафывафыва")


@bot.message_handler(commands=['exchange'])
def exchange_command(message):
    """
    Выводит на экран меню с кнопками, которые позволяют выбрать валюту для проверки курса валют
    """
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('USD', callback_data="USD"),
                 telebot.types.InlineKeyboardButton(
                     'EUR', callback_data="EUR"),
                 telebot.types.InlineKeyboardButton(
                     'RUB', callback_data="RUB"),
                 )
    bot.send_message(chat_id=message.chat.id,
                     text="Click on the currency of choice:", reply_markup=keyboard)


@bot.callback_query_handler(func=check_currency)
def get_exchange_callback(query):
    """
    Функция, котрая возвращает курс валют для выбранной кнопки(валюты)
    """
    # чтобы знать id чата, в котором был запрос
    message = query.message
    # информация от нажатия кнопки
    text = query.data
    # индикатор typing пока происходит запрос в банк
    bot.send_chat_action(message.chat.id, 'typing')
    # убрать состояние загрузки бота
    bot.answer_callback_query(query.id)
    currency = information.get_exchange(text)
    bot.send_message(chat_id=message.chat.id,
                     text=f"{currency['Quantity']} -> {currency['Value to BYN']} "
                     )


@bot.callback_query_handler(func=check_exchange)
def exchange_command_from_start(query):
    """
    Функция, которая на отклик кнопки 'Currency exchange' отправляет пользователю меню

    """
    #bot.send_message(chat_id=query.message.chat.id, text=f"{query.data}")
    bot.answer_callback_query(query.id)
    exchange_command(query.message)


@bot.inline_handler(func=lambda query: True)
def query_text(query):
    pass


bot.polling()
