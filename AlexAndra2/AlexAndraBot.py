import telebot
from telebot import types
import os
import sqlite3
from telebot import apihelper
import pickle


# Pour ne pas mettre les token en clair dans le code
# Charge le token depuis un fichier local

if os.path.exists("botTokenFileActive.pickle"):
    with open('botTokenFileActive.pickle',"rb") as tokenFile:
        botToken = pickle.load(tokenFile)
else:
    print("BotTokenFileActive.pickle not found. Exiting")
    exit()



pdfPath = os.getcwd() + r'\bot telegram messenger.pdf'
bot = telebot.TeleBot(botToken)

# On défini maintenant les boutons d'accueil car ils vont servir a plusieurs endroits du programme !
markupStart = types.ReplyKeyboardMarkup()
conceptBtn = types.KeyboardButton('/concept')
registerBtn = types.KeyboardButton('/register')
partnerBtn = types.KeyboardButton('/partners')
tutosBtn = types.KeyboardButton('/brokers')
tarifsBtn = types.KeyboardButton('/prices')
moreBtn = types.KeyboardButton('/more')
supportBtn = types.KeyboardButton('/support')
languageBtn = types.KeyboardButton('/language')

markupStart.row(conceptBtn, registerBtn, partnerBtn)
markupStart.row(tutosBtn, tarifsBtn, moreBtn)
markupStart.row(supportBtn, languageBtn)





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
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
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
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
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

    answer = "Langage pour "+ str(message.from_user.first_name) +" "+str(message.from_user.last_name) +" = français !" # On met la réponse dans une variable
    answer = answer.replace('None','') #On enlève les "None" si il y en a
    bot.reply_to(message, answer, reply_markup=markupStart) # On répond ce qui permet de ré-afficher le clavier d'accueil
@bot.message_handler(commands=['🇬🇧'])
def pickGb(message):
    if not checkIfInBDD(message.from_user.id):

        cursor.execute('INSERT INTO users VALUES(?,?)', (message.from_user.id, '🇬🇧'))


    else:
        cursor.execute('UPDATE users SET language = ? WHERE userId == ?' , ('🇬🇧' ,message.from_user.id))
    conn.commit()

    answer = "Language for "+ str(message.from_user.first_name) +" "+str(message.from_user.last_name) +" = english !" # On met la réponse dans une variable
    answer = answer.replace('None','') #On enlève les "None" si il y en a
    bot.reply_to(message, answer, reply_markup=markupStart) # On répond ce qui permet de ré-afficher le clavier d'accueil
@bot.message_handler(commands=['🇪🇸'])
def pickEs(message):
    if not checkIfInBDD(message.from_user.id):

        cursor.execute('INSERT INTO users VALUES(?,?)', (message.from_user.id, '🇪🇸'))


    else:
        cursor.execute('UPDATE users SET language = ? WHERE userId == ?', ('🇪🇸', message.from_user.id))
    conn.commit()
    answer = "Idioma para "+ str(message.from_user.first_name) +" "+str(message.from_user.last_name) +" = Español !" # On met la réponse dans une variable
    answer = answer.replace('None','') #On enlève les "None" si il y en a
    bot.reply_to(message, answer, reply_markup=markupStart) # On répond ce qui permet de ré-afficher le clavier d'accueil







''' 
*******************************************************
---------------------COMMANDES-------------------------
*******************************************************
'''


@bot.message_handler(commands=['start']) #Répond a la commande /Start
def start(message):

    # Boutons d'accueil (markupStart) défini au début du programme

    if botLanguage == 'french': # Commande Start en fr
        bot.reply_to(message, "Bonjour, ceci est le bot d'aide en phase de développement. De quoi avez vous besoin ?", reply_markup=markupStart)

    elif botLanguage == 'english': #Commande Start en anglais
        bot.reply_to(message, "Hello, the bot is in dev stage, what do you need ?", reply_markup=markupStart)

    elif botLanguage == "spanish":
        bot.reply_to(message, "Hola, este es el bot de ayuda de la etapa de desarrollo. Qué necesita ?", reply_markup=markupStart)


@bot.message_handler(commands=['concept'])
def concept(message):
    if botLanguage == 'french':
        bot.reply_to(message, "Quel est le concept ?\nVoici une vidéo de présentation !\nhttps://www.fenixtradauto.com/presentation/")
        bot.reply_to(message, "<PDF>")

    elif botLanguage == 'english':
        bot.reply_to(message, "How it works ?\n"
                              "Here the presentation:\n"
                              "https://www.fenixtradauto.com/presentation/")
        #bot.reply_to(message, "<PDF>")
    elif botLanguage == "spanish":
        bot.reply_to(message, "Como funciona ?\n"
                              "https://www.fenixtradauto.com/presentacion/")
        #bot.reply_to(message, "<PDF>")




@bot.message_handler(commands=['register'])
def register(message):
    if botLanguage == 'french':
        bot.reply_to(message, "Comment s'inscrire ?\nVoici une vidéo tutorielle:\nhttps://www.fenixtradauto.com/tutoriels")
    elif botLanguage == 'english':
        bot.reply_to(message, "How to register ?\nThis is a tutorial video:\nhttps://www.fenixtradauto.com/tutoriels")
    elif botLanguage == "spanish":
        bot.reply_to(message, "Como registrarse ?\nAquí podrás seguir los pasos:\nhttps://www.fenixtradauto.com/tutoriales")


@bot.message_handler(commands=['partners'])
def partner(message):
    if botLanguage == 'french':
        bot.reply_to(message,
                     "Liens partenaires:\n"
                     "Si vous résidez en France ou Portugal, veuillez utiliser ce lien\nhttp://go.vantagefx.com/visit/?bta=35651&nci=5492\n\n"
                     "Si vous résidez en Belgique, Espagne, DOM TOM, Japon, veuillez utiliser ce lien\nhttps://www.ironfx.com/fr/register?utm_source=13087357&utm_medium=ib_link&utm_campaign=IB\n\n"
                     "Si vous résidez au Canada, veuillez utiliser ce lien\nhttps://www.usgfx.global/RegAcc/RegAccStep1?culture=fr-FR&IB=2128p8R808R8Q8R-0f")
    elif botLanguage == 'english':
        bot.reply_to(message,
                     "Partner links:\n"
                     "If you live in France or Portugal please use this link\nhttp://go.vantagefx.com/visit/?bta=35651&nci=5492\n\n"
                     "If you live in Belgium, Spain, Overseas - Departments and territories, Japan, please use this link\nhttps://www.ironfx.com/fr/register?utm_source=13087357&utm_medium=ib_link&utm_campaign=IB\n\n"
                     "If you live in Canada, please use this link\nhttps://www.usgfx.global/RegAcc/RegAccStep1?culture=fr-FR&IB=2128p8R808R8Q8R-0f")
    elif botLanguage == "spanish":
        bot.reply_to(message,
                     "Liens partenaires:\n"
                     "Si vives en Francia o en Portugal tienes que registrarte con este link\nhttp://go.vantagefx.com/visit/?bta=35651&nci=5492\n\n"
                     "Si resides en Belgica, España, en DOM TOM, o en Japon tienes que registrarte por allí\nhttps://www.ironfx.com/fr/register?utm_source=13087357&utm_medium=ib_link&utm_campaign=IB\n\n"
                     "Si resides en Canada, tienes que registrarte con este link\nhttps://www.usgfx.global/RegAcc/RegAccStep1?culture=fr-FR&IB=2128p8R808R8Q8R-0f")




@bot.message_handler(commands=['brokers'])
def tutorials(message):
    if botLanguage == 'french':
        bot.reply_to(message,"Tout les brokers sont regroupés ici, attention de bien vérifier avec notre support s'il est compatible avec votre profil:\n"
                             "https://www.fenixtradauto.com/brokers")
    elif botLanguage == 'english':
        bot.reply_to(message,"All brokers are here grouped, pay attention to check our support if it’s compatible with you profile:\n"
                             "https://www.fenixtradauto.com/brokers")
    elif botLanguage == "spanish":
        bot.reply_to(message,"Todos los brokers están mencionados en este PDF, hay que verificar con el soporte si es compatible con tu perfil:\n"
                             "https://www.fenixtradauto.com/brokers")



@bot.message_handler(commands=['prices'])
def tarifs(message):
    if botLanguage == 'french':
        bot.reply_to(message, "<IMAGE ABONNEMENT>\n"
                              "https://www.fenixtradauto.com/abostarter/\n"
                              "<PHOTO ICONE ABONNEMENT>")

    elif botLanguage == 'english':
        bot.reply_to(message, "<IMAGE ABONNEMENT>\n"
                              "https://www.fenixtradauto.com/abostarter/\n"
                              "<PHOTO ICONE ABONNEMENT>")
    elif botLanguage == "spanish":
        bot.reply_to(message, "<IMAGE ABONNEMENT>\n"
                              "https://www.fenixtradauto.com/abostarter/\n"
                              "<PHOTO ICONE ABONNEMENT>")




@bot.message_handler(commands=['more'])
def more(message):

    if botLanguage == 'french':
        bot.reply_to(message, "Pour en savoir plus:\n"
                              "- visitez le site: https://fenixtradauto.com\n"
                              "- abonnez vous à la chaine: https://youtube.com/c/FenixTradAuto")
    elif botLanguage == 'english':
        bot.reply_to(message, "To know more about it:\n"
                              "- have a look of our website: https://fenixtradauto.com\n"
                              "- Subscribe to our channel: https://youtube.com/c/FenixTradAuto")
    elif botLanguage == "spanish":
        bot.reply_to(message, "Para mas informacíon:\n"
                              "- Visitar las pagina web: https://fenixtradauto.com\n"
                              "- Seguir el Canal Youtube: https://youtube.com/c/FenixTradAuto")



@bot.message_handler(commands=['support'])
def support(message):
    if botLanguage == 'french':
        bot.reply_to(message, "Support:\n"
                              "Voici le lien du support:\nhttps://member.tradingauto.eu/user/helpdesk/tickets-dashboard")
    elif botLanguage == 'english':
        bot.reply_to(message, "Support:\n"
                              "Here the link for our support:\nhttps://member.tradingauto.eu/user/helpdesk/tickets-dashboard")
    elif botLanguage == "spanish":
        bot.reply_to(message, "Support:\n"
                              "El enlace del soporte:\nhttps://member.tradingauto.eu/user/helpdesk/tickets-dashboard")






bot.polling()




''' 
*******************************************************
---------------------TEMPLATES-------------------------
*******************************************************
'''


''' Rajouter une commande:

@bot.message_handler(commands=['commande'])
def commande(message):
    if botLanguage == 'french': #
        None
    elif botLanguage == 'english':
        None
    elif botLanguage == "spanish":
        None



'''

