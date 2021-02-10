import telebot
from telebot import types
import os
import sqlite3
#botToken = "1629958699:AAEeVgua1DTi-gzp6AWtIbdxXHWvPSHFqCc"
botToken = "1632753705:AAHerazoKWTDDtvFpYUjTCf0O61Ggv-Ebe4"

pdfPath = os.getcwd() + r'\bot telegram messenger.pdf'
bot = telebot.TeleBot(botToken)


conn = sqlite3.connect('DataBaseLanguage.db', check_same_thread=False)
cursor = conn.cursor()

try: #Créer la table "Clients" si elle n'existe pas déjà
    cursor.execute('CREATE TABLE users(chatId BIGINT, language TEXT)')
except sqlite3.OperationalError:
    pass

conn.commit() #Enregistre


def checkIfInBDD(user_id):
    cursor.execute('SELECT chatId FROM users')
    result = cursor.fetchall()
    tempBool = False
    for id in result:
        if user_id in id:
            tempBool = True
            break
    return tempBool

def pickLanguage(message):
    markup = types.ReplyKeyboardMarkup()
    frButton = types.KeyboardButton('/🇫🇷')
    enButton = types.KeyboardButton('/🇬🇧')
    esButton = types.KeyboardButton('/🇪🇸')

    markup.row(frButton,enButton,esButton)

    bot.reply_to(message, "Language ?", reply_markup=markup)

@bot.message_handler(commands=['start']) #Répond a la commande /Start
def start(message):

    #if checkIfInBDD(message.from_user.id):
    pickLanguage(message)
    '''
    markup = types.ReplyKeyboardMarkup()
    conceptBtn = types.KeyboardButton('/concept')
    registerBtn = types.KeyboardButton('/register')
    partnerBtn = types.KeyboardButton('/partners')
    tutosBtn = types.KeyboardButton('/tutorials')
    tarifsBtn = types.KeyboardButton('/tarifs')
    moreBtn = types.KeyboardButton('/more')
    supportBtn = types.KeyboardButton('/support')
    markup.row(conceptBtn,registerBtn,partnerBtn)
    markup.row(tutosBtn,tarifsBtn,moreBtn,supportBtn)

    bot.reply_to(message, "Bonjour, ceci est le bot d'aide en phase de développement. De quoi avez vous besoin ?", reply_markup=markup)
    '''
@bot.message_handler(commands=['concept'])
def concept(message):
    bot.reply_to(message, "Voici une vidéo de présentation !\nhttps://youtube.com")
    bot.reply_to(message, "<PDF>")

@bot.message_handler(commands=['register'])
def register(message):
    bot.reply_to(message, "Voici une vidéo expliquant comment s'inscrire !\nhttps://youtube.com")
    bot.reply_to(message, "Voici également un PDF pour ceux qui préfèrent lire\n<PDF>")

@bot.message_handler(commands=['partners'])
def partner(message):
    bot.reply_to(message,
                 "Si vous résidez en France, veuillez utiliser ce lien\nhttps://google.fr\n\n"
                 "Si vous résidez en Belgique, veuillez utiliser ce lien\nhttps://google.fr\n\n"
                 "Si vous résidez dans les DOMTOM, veuillez utiliser ce lien\nhttps://google.fr\n\n"
                 "Si vous résidez en Espagne, au canade, etc... veuillez utiliser ce lien\nhttps://google.fr")

@bot.message_handler(commands=['tutorials'])
def tutorials(message):
    bot.reply_to(message,
                 "Voici les différents tutoriels:\n"
                 "Ouvrir un compte sur un broker:\nhttps://google.fr\n\n"
                 "Telecharger mt4:\nhttps://google.fr\n\n"
                 "Comment faire ci:\nhttps://google.fr\n\n"
                 "Comment faire ça:\nhttps://google.fr\n\n"

                 )

@bot.message_handler(commands=['tarifs'])
def tarifs(message):
    bot.reply_to(message, "<IMAGE>")

@bot.message_handler(commands=['more'])
def more(message):
    bot.reply_to(message,
                 "Visitez le site:\nhttps://google.fr\n"
                 "Abonnez vous à la chaine:\nhttps://youtube.fr")

@bot.message_handler(commands=['support'])
def support(message):
    bot.reply_to(message, "Voici le lien du support:\nhttps://google.fr")

bot.polling()