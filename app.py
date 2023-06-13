import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConvertor

bot = telebot.TeleBot(TOKEN)

#обработчик инструкций
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет! Я Бот-Конвертер валют.\nЧтобы начать работать введите команду боту в следующем формате: \n<имя валюты цену которой нужно узнать> \
<имя валюты в которой надо узнать цену первой валюты> \
<количество первой валюты> \nУвидить список всех доступных валют: /values'
    bot.reply_to(message, text)

#обработчик доступных валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

#обработчик конвертации валют
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        #проверяем на колличество введенных значений (правильно - 1 валюта, 2 валюта, сколько)
        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        guote, base, amount = values
        total_base = CryptoConvertor.get_price(guote, base, amount)
    #обрабатываем исключения
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    #проверка ели неизвесная команда (е - это исключение, которое передаем как обьект)
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    #если все введено верно - выдает текст
    else:
        text = f'Переводим {quote} в {base}\nЦена {amount} {guote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
