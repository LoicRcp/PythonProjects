import pickle
import xlrd
import time

import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from bs4 import BeautifulSoup as bs

import PySimpleGUI as sg

wb = xlrd.open_workbook('Octobre 2020 - MODIFIER.xls')
sheet = wb.sheet_by_index(0)

try:
    with open('creds.pickle', 'rb') as credsFile:
        creds = pickle.load(credsFile)

except:
    print("No creds file in the folder...")
    exit()


def getInfos():
    variables = ['sex', 'nom', 'ville', 'mail', 'rowNb']
    clientList = []
    for i in range(1, sheet.nrows):
        if sheet.cell(i, 15) != 'OK':
            client = {}
            client[variables[0]] = sheet.cell(i, 2).value
            client[variables[1]] = sheet.cell(i, 4).value
            client[variables[2]] = sheet.cell(i, 9).value
            client[variables[3]] = sheet.cell(i, 11).value
            client[variables[4]] = i
            clientList.append(client)
    return clientList




def autoMode(client):

    mail = creds[0]
    password = creds[1]
    # mail = 'test1'
    # password = 'test2'
    sender = mail
    for client in clientList:
        files_to_send = [
            "fichier1.txt",
            "fichier2.txt",
        ]

        receiver = 'darkdiablot@gmail.com'
        subject = client['sex'] + '. ' + client['nom'] + ', vos clients vous cherchent sur internet !'

        msg = MIMEMultipart('alternative')
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject

        html = f'<b>{client["sex"]}.{client["nom"]},\n\n' \
               f'Félicitations pour la création de votre entreprise !</b>\n' \
               f"Lorsque l'on décide d'ouvrir son affaire, il est important de penser à sa visibilité."

        text = bs(html, 'html.parser').text

        text_part = MIMEText(text, "plain")
        html_part = MIMEText(html, "html")
        # attach the email body to the mail message
        # attach the plain text version first
        msg.attach(text_part)
        msg.attach(html_part)

        for file in files_to_send:
            with open(file, 'rb') as f:
                data = f.read()
                attach_part = MIMEBase("application", "octet-stream")
                attach_part.set_payload(data)
                encoders.encode_base64(attach_part)
                attach_part.add_header("Content-Disposition", f"attachment; filename= {file}")
                msg.attach(attach_part)

        # send_mail(mail, password, sender, receiver, msg)
        print(f'Envoi du mail a {receiver}')
        print('\n' + msg.as_string())



def makeMail(client):
    files_to_send = [
        "fichier1.txt",
        "fichier2.txt",
    ]

    receiver = 'darkdiablot@gmail.com'
    subject = client['sex'] + '. ' + client['nom'] + ', vos clients vous cherchent sur internet !'

    msg = MIMEMultipart('alternative')
    msg['From'] = creds[0]
    msg['To'] = receiver
    msg['Subject'] = subject

    html = f'<b>{client["sex"]}.{client["nom"]},\n\n' \
           f'Félicitations pour la création de votre entreprise !</b>\n' \
           f"Lorsque l'on décide d'ouvrir son affaire, il est important de penser à sa visibilité."

    text = bs(html, 'html.parser').text

    text_part = MIMEText(text, "plain")
    html_part = MIMEText(html, "html")
    # attach the email body to the mail message
    # attach the plain text version first
    msg.attach(text_part)
    msg.attach(html_part)

    for file in files_to_send:
        with open(file, 'rb') as f:
            data = f.read()
            attach_part = MIMEBase("application", "octet-stream")
            attach_part.set_payload(data)
            encoders.encode_base64(attach_part)
            attach_part.add_header("Content-Disposition", f"attachment; filename= {file}")
            msg.attach(attach_part)
    return msg


def send_mail(email, password, FROM, TO, msg, rowNb):
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.starttls()
    # server.login(email, password)
    # server.sendmail(FROM, TO, msg.as_string())
    # server.quit()

    print(f'Envoi du mail a {TO}')
    print('\n' + msg.as_string())

    #sheet.cell(rowNb, 15).value = 'OK'

sg.theme('Dark')
layout = [
    [sg.Text('Sexe'), sg.InputText(size=(5, 1),key='sex'), sg.Text('Nom'), sg.InputText(size=(15, 1),key='name'), sg.Text('Ville'),
     sg.InputText(size=(20, 1),key='city'), sg.Text('Mail'), sg.InputText(size=(30, 1),key='mail')],
    [sg.Text('___________________________________________'),
     sg.Button("Confirmer", button_color=('#1c1c1c', '#9b9b9b'),key='confirm'),
     sg.Text('___________________________________________')],
    [sg.Text('Delai (s):'), sg.InputText('30',size=(5, 1),key='delai'),
     sg.Button("Envoi de mails", size=(13, 1), button_color=('#1c1c1c', '#9b9b9b'), key='sendMail'),
     sg.Button("Stop", size=(13, 1), button_color=('#1c1c1c', '#9b9b9b'), key='stopMail'),
     sg.VerticalSeparator(),
     sg.Button('Création de Words', size=(41, 1), button_color=('#1c1c1c', '#9b9b9b'), key='word')],
    [sg.Text('_' * 99)],
    [sg.Output(size=(96, 10), echo_stdout_stderr=True)]

]

window = sg.Window("mailSender", layout)





sendingMail = False
endTime = time.time()

clientList = None
clientNumber = 0
delay = 30

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Quitter":
        break




    if event == 'sendMail':
        sendingMail = True
        delay = values['delai']
        endTime = int(time.time()) + int(delay)
        clientList = getInfos()

        window.Element('sex').Update(clientList[0]['sex'])
        window.Element('name').Update(clientList[0]['nom'])
        window.Element('city').Update(clientList[0]['ville'])
        window.Element('mail').Update(clientList[0]['mail'])

        print(f'Starting in {delay}s...')


    nowTime = int(time.time())
    while sendingMail:
        event,values = window.read(1000)
        if int(time.time()) > endTime:
            client = clientList[clientNumber]

            window.Element('sex').Update(client['sex'])
            window.Element('name').Update(client['nom'])
            window.Element('city').Update(client['ville'])
            window.Element('mail').Update(client['mail'])

            msg = makeMail(client)
            send_mail(creds[0], creds[1], creds[0], 'darkdiablot@gmail.com', msg, client['rowNb'])
            endTime = int(time.time()) + int(time.time())+int(delay)
            clientNumber+=1
        if event == 'stopMail':
            sendingMail = False
            print("Stop...")
            window.Element('sex').Update('')
            window.Element('name').Update('')
            window.Element('city').Update('')
            window.Element('mail').Update('')

        if event == 'confirm':
            clientSex = values['sex']
            clientNom = values['name']
            clientVille = values['city']
            clientMail = values['mail']


# clientList = getInfos()
# autoMode()
