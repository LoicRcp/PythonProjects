import telebot
from telebot import types

#botToken = "1629958699:AAEeVgua1DTi-gzp6AWtIbdxXHWvPSHFqCc"
botToken = "1632753705:AAHerazoKWTDDtvFpYUjTCf0O61Ggv-Ebe4"

bot = telebot.TeleBot(botToken)

@bot.message_handler(commands=['start']) #Répond a la commande /Start
def start(message):
    markup = types.ReplyKeyboardMarkup()
    conceptBtn = types.KeyboardButton('/concept')
    registerBtn = types.KeyboardButton('/register')
    partnerBtn = types.KeyboardButton('/partner')
    tutosBtn = types.KeyboardButton('/tutorials')
    tarifsBtn = types.KeyboardButton('/tarifs')
    moreBtn = types.KeyboardButton('/more')
    supportBtn = types.KeyboardButton('/support')
    markup.row(conceptBtn,registerBtn,partnerBtn)
    markup.row(tutosBtn,tarifsBtn,moreBtn,supportBtn)

    bot.reply_to(message, "Bonjour, ceci est le bot d'aide en phase de développement. De quoi avez vous besoin ?", reply_markup=markup)



bot.polling()