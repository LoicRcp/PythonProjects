
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
    with open('creds.pickle','rb') as credsFile:
        creds = pickle.load(credsFile)

except:
    print("No creds file in the folder...")
    exit()


def getInfos():
    variables = ['sex','nom','ville','mail','colNb']
    clientList = []
    for i in range(1, sheet.nrows):
        if sheet.cell(i, 15) != 'OK':
            client = {}
            client[variables[0]] = sheet.cell(i,2).value
            client[variables[1]] = sheet.cell(i,4).value
            client[variables[2]] = sheet.cell(i,9).value
            client[variables[3]] = sheet.cell(i,11).value
            client[variables[4]] = i
            clientList.append(client)
    return clientList




def send_mail(email, password, FROM, TO, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()

def autoMode():
    mail = creds[0]
    password = creds[1]
    #mail = 'test1'
    #password = 'test2'
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
                attach_part = MIMEBase("application","octet-stream")
                attach_part.set_payload(data)
                encoders.encode_base64(attach_part)
                attach_part.add_header("Content-Disposition", f"attachment; filename= {file}")
                msg.attach(attach_part)


        send_mail(mail,password,sender,receiver,msg)
        exit()

sg.theme('Dark')
layout = [
    [sg.Text('Sexe'), sg.InputText(size=(10,1)),sg.Text('Nom'), sg.InputText(size=(15,1)),sg.Text('Ville'), sg.InputText(size=(15,1)),sg.Text('Mail'), sg.InputText(size=(30,1))],
    [sg.Text('___________________________________________'),sg.Button("Confirmer"),sg.Text('___________________________________________')],
    [sg.Text('Delai (s):'), sg.InputText(size=(5,1)), sg.Button("Envoi de mails"), sg.Button('Création de Words')]






          ]

window = sg.Window("mailSender", layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Quitter":
        break

clientList = getInfos()
autoMode()