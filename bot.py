import telebot
import config
import info

bot = telebot.TeleBot(config.TOKEN)
information = info.CityInfo() #интерфейс взаимодействия с различными API


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Hi! You can use the /exchange functions. New ones will be added soon!")


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(
        'Message the developer', url='https://telegram.me/jkban4e'
    ))
    bot.send_message(chat_id=message.chat.id, text='The /exchange functions are now available. New ones will be added soon!',
                     reply_markup=keyboard
                     )


@bot.message_handler(commands=['exchange'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(
                'USD', callback_data="USD"),
                telebot.types.InlineKeyboardButton(
                'EUR', callback_data="EUR"),
                telebot.types.InlineKeyboardButton(
                'RUB', callback_data="RUB"),
                )
    bot.send_message(chat_id=message.chat.id,
                     text="Click on the currency of choice:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def get_exchange_callback(query):
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


@bot.inline_handler(func=lambda query: True)
def query_text(query):
    pass


bot.polling()
