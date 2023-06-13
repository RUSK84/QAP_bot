import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConvertor

bot = telebot.TeleBot(TOKEN)

#обработчик инструкций
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет! Я Бот-Конвертер валют и я могу:  \n- Показать список доступных валют через команду /values \
    \n- Вывести конвертацию валюты через команду <имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n \
- Напомнить, что я могу через команду /help'
    bot.reply_to(message, text)
    
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию, введите команду боту в следующем формате: \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\nЧтобы увидеть список всех доступных валют, введите команду\n/values'
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
            raise ConvertionException('Введите команду или 3 параметра')

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
