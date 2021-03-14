import pickle
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.tl.types import ChannelParticipantsRecent, ChannelParticipantsSearch
from telethon import functions
from telethon.errors.rpcerrorlist import PeerFloodError, UserNotMutualContactError, UserPrivacyRestrictedError, UserChannelsTooMuchError, ChatAdminRequiredError, ChatForbiddenError
import telethon.tl
import PySimpleGUI as sg
import csv
import os

try:
    with open('creds.pickle', 'rb') as credsFile:
        creds = pickle.load(credsFile)

except:
    print("No creds file in the folder...")
    exit()




api_id = creds[0]
api_hash = creds[1]
phoneNb = creds[2]

def connect():
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(creds[2])
        client.sign_in(creds[2], input('Entrer le code:'))
    print("--CONNECT: OK--")

client = TelegramClient(phoneNb, api_id, api_hash)


def getgroups():
    chats = client.get_dialogs()
    groups = []
    for chat in chats:
        try:
         if (chat.is_channel or chat.is_group):
            groups.append(chat.entity)
        except Exception as e:
            print("Erreur: ",e)

    print("--GETGROUPS: OK--")
    return groups



def getMembers(mode, target_groups):
    membersList = []
    for group in target_groups:


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
                        membersList.append([user.id, user.first_name, user.last_name, user.username, group.title])
                except ChatAdminRequiredError:
                    print("ERREUR: Il faut être admin pour récupérer les membres de ce groupe.")
                except Exception as e:
                    print(e)
    return membersList

def listToCsv(list, csvName):
    with open(csvName+'.csv', "w", newline="", encoding="UTF-8") as f:
        writer = csv.writer(f)

        writer.writerows(list)




connect()

layout = \
[
[sg.Listbox(values='',size=(66, 6), key=("ListBox"), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
[sg.Button("Demarrer l'export", size=(59,1), button_color=('#1c1c1c','#9b9b9b'))],
[sg.Text("___________________________________________________________________")],
[sg.Output(size=(66, 10), echo_stdout_stderr=True)]
]

window = sg.Window("TelegramScraperInterface", layout, finalize=True)

mode =1


groupList = getgroups()
toShowList = []
for group in groupList:
    toShowList.append(group.title)
window['ListBox'].update(toShowList)


while True:
    event, values = window.read()





    if event == sg.WIN_CLOSED or event == "Quitter":
        break
    if event == "Demarrer l'export":
        try:
            listBoxOutput = values['ListBox']

            for group in groupList:
                if group.title in listBoxOutput:
                    chosenGroup = group

            with open("group.pickle", "wb") as file:
                pickle.dump(chosenGroup, file)

            print(f"Export du groupe {chosenGroup.title} réussi !")
        except Exception as e:
            print(e)

