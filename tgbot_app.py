import telebot
from tgbot_config import keys, TOKEN
from tgbot_extensions import APIException, CriptoConvertor

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['values'])    #показывает список доступных валют
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(commands = ['start', 'help'])   #выводит инфо
def help(message: telebot.types.Message):
    text = 'Что бы начать работу введите команду боту в следующем формате: \n <имя валюты><в какую валюту перевести><количество переводимой валюты> \n' \
'Пример: доллар евро 5 \n' \
'Что бы увидеть список валют введите /values'
    bot.reply_to(message, text)


@bot.message_handler(content_types = ['text'])    #конвертирует валюты
def convert(message: telebot.types.Message):
    try:
        values = [i.lower() for i in message.text.split(' ')]

        if len(values) != 3:
            raise APIException('Слишком много/мало параметров.\nинструкция по команде /help')

        quote, base, amount = values
        total_base = CriptoConvertor.get_price(quote, base, amount)

    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя. \n{e}')

    except Exception as e:
        bot.send_message(message.chat.id, f'Непредвиденная ошибка. \n{e}')
    else:
        text = f"Цена {amount} {quote}(а) в {base} равна {total_base} {base}"
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types = ['photo'])   #отвечает на фото
def repeat_photo(message: telebot.types.Message):
    bot.reply_to(message, f"{message.chat.username}, пожалуйста без фото")

#@bot.message_handler(content_types = ['text'])   # отвечает на текст
#def repeat(message: telebot.types.Message):
#    bot.send_message(message.chat.id, f"{message.chat.username}, тест")

bot.polling(none_stop=True)
