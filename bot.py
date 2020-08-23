import telebot
import config
import requests
from bs4 import BeautifulSoup
import urllib

bot = telebot.TeleBot(config.token)

markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
markup.add('Расписание 📅')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '✋', reply_markup=markup)


@bot.message_handler(commands=['ras'])
def print_ras(message):
    get_ras_pdf()
    file = open('Расписание.pdf', 'rb')
    bot.send_message(message.chat.id, 'Вот держи свое расписание 📅', reply_markup=markup)
    bot.send_document(message.chat.id, file, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Расписание 📅':
        get_ras_pdf()
        file = open('Расписание.pdf', 'rb')
        bot.send_message(message.chat.id, 'Вот держи свое расписание 📅', reply_markup=markup)
        bot.send_document(message.chat.id, file, reply_markup=markup)


def get_ras_pdf():
    URL = 'http://mtec.by/67/103/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', id='content')
    LINK = 'http://mtec.by' + items[0].find('a', target='_blank').get('href')
    urllib.request.urlretrieve(LINK, "Расписание.pdf")


if __name__ == '__main__':
    bot.polling()
