import pickle
import telebot
import sqlite3
from telebot import apihelper

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.tl.types import ChannelParticipantsRecent, ChannelParticipantsSearch
from telethon import functions
from telethon.errors.rpcerrorlist import PeerFloodError, UserNotMutualContactError, UserPrivacyRestrictedError, UserChannelsTooMuchError, ChatAdminRequiredError, ChatForbiddenError
import telethon.tl

import threading


try:
    with open('creds.pickle', 'rb') as credsFile:
        creds = pickle.load(credsFile)

except:
    print("No creds file in the folder...")
    exit()


api_id = creds[0]
api_hash = creds[1]
phoneNb = creds[2]
botToken = creds[3]




conn = sqlite3.connect('DataBaseClients.db', check_same_thread=False)
cursor = conn.cursor()

try: #Créer la table "Clients" si elle n'existe pas déjà
    cursor.execute('CREATE TABLE clients(firstName TEXT,lastName TEXT, username TEXT, chatId BIGINT, subDateStart DATE, subDateEnd DATE)')
except sqlite3.OperationalError:
    pass
conn.commit() #Enregistre







# Connect to client API
def connect():
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(creds[2])
        client.sign_in(creds[2], input('Entrer le code:'))
    print("--CONNECT: OK--")

def updateMembersBdd():
    None

# Bot polling pour le multiThreading
def botPolling():
    bot.polling()

client = TelegramClient(phoneNb, api_id, api_hash)
connect()


bot = telebot.TeleBot(botToken)
updateMembersBdd()



t2 = threading.Thread(target=botPolling)
t2.start()