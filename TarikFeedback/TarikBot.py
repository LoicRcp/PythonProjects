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

try:
    with open('group.pickle', 'rb') as groupFile:
        group = pickle.load(groupFile)

except:
    print("No group file in the folder...")
    exit()


conn = sqlite3.connect('DataBaseClients.db', check_same_thread=False)
cursor = conn.cursor()

try: #Créer la table "Clients" si elle n'existe pas déjà
    cursor.execute('CREATE TABLE clients(firstName TEXT,lastName TEXT, username TEXT, userId BIGINT, subDateStart DATE, subDateEnd DATE)')
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

def getgroups():
    chats = client.get_dialogs()
    groups = []
    for chat in chats:
        try:
         if (chat.is_channel or chat.is_group):
            groups.append(chat.entity)
        except Exception as e:
            print("Erreur: ",e)
    return groups
def getMembers(mode, group):


    membersList = []



    if type(group) == telethon.tl.types.Chat:
        participants = (client.get_participants(entity=group.id))
        for user in participants:
            membersList.append([user.id, user.first_name, user.last_name, user.username, group.title])

    elif type(group) == telethon.tl.types.Channel or group.megagroup:

        if mode == 1:

            offset = 0
            limit = 1000000

            while True:

                try:


                    participants = client(GetParticipantsRequest(
                        group, ChannelParticipantsSearch(''), offset, limit,
                        hash=0,
                    ))

                    if not participants.users:
                        break
                    for user in participants.users:
                        membersList.append([user.id, user.first_name, user.last_name, user.username, group.title, user.access_hash])
                    offset += len(participants.users)
                except ChatAdminRequiredError:
                    print("ERREUR: Il faut être admin pour récupérer les membres de ce groupe.")
                    break

        elif mode == 2:
            try:
                #participants = client.iter_participants(group,limit=100000,aggressive=True)
                for user in client.iter_participants(group,limit=100000,aggressive=True):
                    membersList.append([user.id, user.first_name, user.last_name, user.username, group.title, user.access_hash])
            except ChatAdminRequiredError:
                print("ERREUR: Il faut être admin pour récupérer les membres de ce groupe.")
            except Exception as e:
                print(e)
    return membersList


def checkIfInBDD(user_id):
    cursor.execute('SELECT userId FROM clients')
    result = cursor.fetchall()
    tempBool = False
    for id in result:
        if user_id in id:
            tempBool = True
            break
    return tempBool

def checkIfInMemberList(memberList, userToFind):
    tempBool = False
    for user in memberList:
        if user == userToFind:
            tempBool = True
            break
    return tempBool

def updateMembersBdd():
    groupId = group.id
    for groups in getgroups():
        if groups.id == groupId:
            chosenGroup = groups
            break

    memberList1 = getMembers(1, chosenGroup)
    memberList2 = getMembers(2, chosenGroup)



    memberList1.sort()
    memberList2.sort()

    mergedMemberList = memberList1
    mergedMemberList.extend(x for x in memberList2 if x not in mergedMemberList)

    cursor.execute('SELECT * FROM clients')
    bddMembers = cursor.fetchall()

    bddMembers.sort()
    mergedMemberList.sort()

    inMemberGroupNotInBdd = []


    for i in range(len(mergedMemberList)):
        setted = mergedMemberList[i][0]
        inBdd = False
        for j in range(len(bddMembers)):
            setted2 = bddMembers[j][3]
            if setted == setted2:
                inBdd = True
                break
        if not inBdd:
            inMemberGroupNotInBdd.append(mergedMemberList[i])




    inBddNotInMemberGroup = []

    for i in range(len(bddMembers)):
        setted = bddMembers[i][3]
        inMemberList = False
        for j in range(len(mergedMemberList)):
            setted2 = mergedMemberList[j][0]
            if setted == setted2:
                inMemberList = True
                break
        if not inMemberList:
            inBddNotInMemberGroup.append(bddMembers[i])

    for user in inBddNotInMemberGroup:
        cursor.execute(f'DELETE FROM clients WHERE userId = {user[3]}')
    # 0 = id
    # 1 = firstname
    # 2 = lastname
    # 3 = username
    # 4 = groupfrom
    # 5 = accesshash
    for user in inMemberGroupNotInBdd:
        cursor.execute(f'INSERT INTO clients VALUES(?,?,?,?,?,?)', (user[1], user[2], user[3], user[0],None, None))
    conn.commit()

    print("NewMember:" )
    for user in inMemberGroupNotInBdd:
        print(user[1],",")
    print("Member who leaved: ")
    for user in inBddNotInMemberGroup:
        print(user[0],",")

    return inMemberGroupNotInBdd

def sendWelcome(newMembers):
    if len(newMembers) > 0:
        welcomeMessage = "Bienvenue au nouveaux membres:\n"
        for member in newMembers: welcomeMessage+=f'{member[1]},\n'
        bot.send_message('-100' + str(group.id), welcomeMessage) # -100 au début du chatId pour dire que c'est un channel




# Bot polling pour le multiThreading
def botPolling():
    bot.polling()

client = TelegramClient(phoneNb, api_id, api_hash)
connect()


bot = telebot.TeleBot(botToken)
sendWelcome(updateMembersBdd())



t2 = threading.Thread(target=botPolling)
t2.start()