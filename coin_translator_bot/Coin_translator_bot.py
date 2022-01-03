import telebot
import config
import utils
'''@Coin_translator_bot'''
'''API: https://freecurrencyapi.net/'''
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helpy(message):
    text = 'Для начала работы введите комманду: \n<название валюты>' \
           '<в какую валюту переводим> <колличество переводимой валюты (дробная величина через точку)>' \
           '\nСписок доступных валют: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message):
    text1 = 'Доступные валюты:'
    for key in config.coin_base:
        text1 = text1 + f'\n{str(key)}'
    bot.send_message(message.chat.id, text1)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        vall = message.text.split(' ')
        if len(vall) != 3:
            raise utils.ConvertionExeptions('Не корректные данные')
        quote, base, amount = vall
        text = utils.RateConverter.converts(quote, base, amount)
        bot.send_message(message.chat.id, f'{amount} {quote} = {round(text*float(amount), 5)} {base}')
    except utils.ConvertionExeptions as error:
        bot.reply_to(message, f'Не удалось выпонить: {error}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить комманду: {e}')


bot.polling(non_stop=True)
