import telebot
from telebot import types
import os
import sqlite3
from telebot import apihelper

#botToken = "1629958699:AAEeVgua1DTi-gzp6AWtIbdxXHWvPSHFqCc"
botToken = "1632753705:AAHerazoKWTDDtvFpYUjTCf0O61Ggv-Ebe4"

pdfPath = os.getcwd() + r'\bot telegram messenger.pdf'
bot = telebot.TeleBot(botToken)


''' 
*******************************************************
---------------------LANGAGE/BDD-----------------------
*******************************************************
'''





conn = sqlite3.connect('DataBaseLanguage.db', check_same_thread=False)
cursor = conn.cursor()

try: #Créer la table "Clients" si elle n'existe pas déjà
    cursor.execute('CREATE TABLE users(userId BIGINT, language TEXT)')
except sqlite3.OperationalError:
    pass

conn.commit() #Enregistre

botLanguage = 'fr'
def checkIfInBDD(user_id):
    cursor.execute('SELECT userId FROM users')
    result = cursor.fetchall()
    tempBool = False
    for id in result:
        if user_id in id:
            tempBool = True
            break
    return tempBool

apihelper.ENABLE_MIDDLEWARE = True
@bot.middleware_handler(update_types=['message'])
def pickLanguage(bot_instance,message):
    if '/' in message.text and not ('🇫🇷' or '🇬🇧' or '🇪🇸') in message.text:

        userId = message.from_user.id
        inBdd = checkIfInBDD(userId)
        if not inBdd:
            markup = types.ReplyKeyboardMarkup()
            frButton = types.KeyboardButton('/🇫🇷')
            enButton = types.KeyboardButton('/🇬🇧')
            esButton = types.KeyboardButton('/🇪🇸')
            markup.row(frButton,enButton,esButton)
            bot.reply_to(message, "Language ?", reply_markup=markup)
        else:

            languageEmoji = cursor.execute('SELECT language FROM users WHERE userId == '+ str(userId)) #On va chercher dans la BDD le langage associé a cet utilisateur
            languageEmoji = languageEmoji.fetchall()[0][0] #ça nous sort le résultat, dans un tableau puis dans un tuple, donc pour le chercher on fait [0][0]
            global  botLanguage
            if languageEmoji == '🇫🇷': #On regarde c'est quel language et on règle la langue du bot en fonction
                botLanguage = 'french'
            elif languageEmoji == '🇬🇧':
                botLanguage = 'english'
            elif languageEmoji == '🇪🇸':
                botLanguage = 'spanish'

@bot.message_handler(commands=['language'])
def pickLanguage(message):
    markup = types.ReplyKeyboardMarkup()
    frButton = types.KeyboardButton('/🇫🇷')
    enButton = types.KeyboardButton('/🇬🇧')
    esButton = types.KeyboardButton('/🇪🇸')
    markup.row(frButton,enButton,esButton)
    bot.reply_to(message, "Language ?", reply_markup=markup)


@bot.message_handler(commands=['🇫🇷'])
def pickFr(message):
    if not checkIfInBDD(message.from_user.id):

        cursor.execute('INSERT INTO users VALUES(?,?)', (message.from_user.id, '🇫🇷'))


    else:
        cursor.execute('UPDATE users SET language = ? WHERE userId == ?' , ('🇫🇷' ,message.from_user.id))
    conn.commit()
@bot.message_handler(commands=['🇬🇧'])
def pickGb(message):
    if not checkIfInBDD(message.from_user.id):

        cursor.execute('INSERT INTO users VALUES(?,?)', (message.from_user.id, '🇬🇧'))


    else:
        cursor.execute('UPDATE users SET language = ? WHERE userId == ?' , ('🇬🇧' ,message.from_user.id))
    conn.commit()
@bot.message_handler(commands=['🇪🇸'])
def pickEs(message):
    if not checkIfInBDD(message.from_user.id):

        cursor.execute('INSERT INTO users VALUES(?,?)', (message.from_user.id, '🇪🇸'))


    else:
        cursor.execute('UPDATE users SET language = ? WHERE userId == ?', ('🇪🇸', message.from_user.id))
    conn.commit()








''' 
*******************************************************
---------------------COMMANDES-------------------------
*******************************************************
'''


@bot.message_handler(commands=['start']) #Répond a la commande /Start
def start(message):


    markup = types.ReplyKeyboardMarkup()
    conceptBtn = types.KeyboardButton('/concept')
    registerBtn = types.KeyboardButton('/register')
    partnerBtn = types.KeyboardButton('/partners')
    tutosBtn = types.KeyboardButton('/tutorials')
    tarifsBtn = types.KeyboardButton('/tarifs')
    moreBtn = types.KeyboardButton('/more')
    supportBtn = types.KeyboardButton('/support')
    languageBtn = types.KeyboardButton('/language')
    markup.row(conceptBtn,registerBtn,partnerBtn,tutosBtn)
    markup.row(tarifsBtn,moreBtn,supportBtn,languageBtn)

    if botLanguage == 'french':
        bot.reply_to(message, "Bonjour, ceci est le bot d'aide en phase de développement. De quoi avez vous besoin ?", reply_markup=markup)

    elif botLanguage == 'english':
        bot.reply_to(message, "Bonjour, ceci est le bot d'aide en phase de développement. De quoi avez vous besoin ?", reply_markup=markup)

    elif botLanguage == "spanish":
        bot.reply_to(message, "Bonjour, ceci est le bot d'aide en phase de développement. De quoi avez vous besoin ?", reply_markup=markup)


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