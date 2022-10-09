import telebot
from config import keys, TOKEN
from extension import ConvertionException, CriptoConverter

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<Имя валюты> \
 <в какую валюту перевести>\
 \n<количество переводимой валюты>\n Увидить список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количесткво параметров!')

        quote, base, amount = values
        total_base = CriptoConverter.convert(quote, base, amount)
        total = float(total_base) * float(amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать комманду.\n {e}')
    else:
        text = f'Цена {amount} {quote} в {base}:  {total}'
        bot.send_message(message.chat.id, text)



bot.polling()


