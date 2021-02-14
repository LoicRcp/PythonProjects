import pickle
import xlrd
from xlutils.save import save

import time
import os

import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from bs4 import BeautifulSoup as bs

import PySimpleGUI as sg



try:
    with open('creds.pickle', 'rb') as credsFile:
        creds = pickle.load(credsFile)

except:
    print("No creds file in the folder...")
    exit()


def getInfos():
    variables = ['sex', 'nom', 'ville', 'mail', 'rowNb']
    clientList = []
    for i in range(2, sheet.nrows):
        if sheet.cell(i, 16).value != 'OK':
            client = {}
            client[variables[0]] = sheet.cell(i, 2).value
            client[variables[1]] = sheet.cell(i, 4).value
            client[variables[2]] = sheet.cell(i, 9).value
            client[variables[3]] = sheet.cell(i, 11).value
            client[variables[4]] = i
            clientList.append(client)
    return clientList






def makeMail(client):
    files_to_send = [
        "N°1 - Pack Site Internet et Hébergement.pdf",
        "N°2 - Sites Fictifs.pdf",
    ]

    receiver = 'darkdiablot@gmail.com'
    subject = client['sex'] + '. ' + client['nom'] + ', vos clients vous cherchent sur internet !'

    msg = MIMEMultipart('alternative')
    msg['From'] = creds[0]
    msg['To'] = receiver
    msg['Subject'] = subject

    signatureImagePath = 'https://ci6.googleusercontent.com/proxy/IS-JCP-uDmQJPIJogh-avP33xvz12vkqqMGgjYINjw0eHHfk5y4KyXy1yQc90TuYHA0NNxoIsAUkTDiCHjJ54CPT3-1anyUWCmRdwaDCqSLHB7fke55qbuJcNvdgbOEr-FGTExcM-8n7uTeZk-n-nrJxSqtMw85xzo9PbiXNWNuTSgmqzJkivZFTOYEdZAG804u3pWGUlvbwENs9-w=s0-d-e1-ft#https://docs.google.com/uc?export=download&id=1qwShh1ZfsGeSvBU-08FhfaRsz5O05YyO&revid=0B33uPyoZhMWSYm0wTXZISm5xRkhQSGhTMWdoODk1NlRGTWQ4PQ'

    html = f'<b>{client["sex"]}.{client["nom"]},\n\n' \
           f'Félicitations pour la création de votre entreprise !</b>\n' \
           f"Lorsque l'on décide d'ouvrir son affaire, il est important de penser à sa visibilité." \
           f"<p>--" \
           f'<tbody><tr><td valign="top" width="100" style="vertical-align: top; --darkreader-inline-outline:#b30000;" title=""><img src="{signatureImagePath}" width="96" height="63" class="CToWUd"></td><td valign="top" style="font-size:1em;padding:0px 0px 0px 15px;vertical-align:top"><table cellspacing="0" cellpadding="0" border="0" style="border-spacing: 0px; border-collapse: collapse; width: 385px; max-width: 400px; line-height: 1.4; font-family: Georgia, serif; font-size: 14.04px; color: rgb(0, 0, 1); --darkreader-inline-color:#e8e6e3;" data-darkreader-inline-color=""><tbody><tr><td style="padding-bottom:4px"><div style="font-family:Georgia,serif"><span style="font-size: 1.2em; color: rgb(42, 42, 42); font-weight: 600; --darkreader-inline-color:#cdc9c3;" data-darkreader-inline-color="">Alexis Sevrin</span><font style="vertical-align:inherit"><font style="vertical-align:inherit">&nbsp;|&nbsp;</font><font style="vertical-align:inherit"><b>Webmaster</b><br></font></font></div></td></tr><tr><td style="padding:1px 0px"><div style="font-family:Georgia,serif"><font style="vertical-align:inherit">|&nbsp;</font><span style="font-weight: 600; color: rgb(42, 42, 42); --darkreader-inline-color:#cdc9c3;" data-darkreader-inline-color="">téléphone:&nbsp;&nbsp;</span>06 25 30 57 11</div></td></tr><tr><td style="padding:1px 0px"><div style="font-family:Georgia,serif"><font style="vertical-align:inherit">|&nbsp;</font><span style="font-weight: 600; color: rgb(42, 42, 42); --darkreader-inline-color:#cdc9c3;" data-darkreader-inline-color="">courriel:&nbsp;&nbsp;</span><a href="mailto:alexissevrin.web@gmail.com" style="color: rgb(0, 0, 1); --darkreader-inline-color:#e8e6e3;" target="_blank" data-darkreader-inline-color="">alexissevrin.web@<wbr>gmail.com</a></div></td></tr></tbody></table></td></tr></tbody></p>'


    html = """<strong>"""+client["sex"]+""". """+ client['nom'] + """,</strong></p>
<p>&nbsp;</p>
<p><strong>F&eacute;licitations pour la cr&eacute;ation de votre entreprise !&nbsp;</strong></p>
<p>Lorsque l'on d&eacute;cide d'ouvrir son affaire, il est important de penser &agrave; sa visibilit&eacute;.</p>
Chaque jour, plus de<strong>&nbsp;6,9 milliards de personnes</strong>&nbsp;recherchent<strong>&nbsp;un service sur Google.</strong><br />Imaginez le potentiel commercial qui s'y cache &agrave; <strong>"""+ client['ville'] +"""</strong> !&nbsp;<br /><br /><strong>85% des internautes contactent un professionnel via le web !<br /></strong>Aujourd'hui, il est donc essentiel d'avoir un site internet pour am&eacute;liorer son image et ses performances commerciales.&nbsp;
<p><br />Vos concurrents l'ont compris, et <strong>absorbent vos clients potentiels</strong>&nbsp;gr&acirc;ce &agrave; leur site internet.<strong><u><br /></u></strong><br /><u>Cr&eacute;er son propre site g&eacute;n&egrave;re &eacute;norm&eacute;ment d'avantages,&nbsp;c'est votre carte de visite digitale</u>&nbsp;:</p>
<ul>
<li><strong>Votre site internet est ouvert 24h/24 et 7j/7 !</strong></li>
<li><strong>Il remplace vos documents publicitaires et r&eacute;duit vos co&ucirc;ts marketing.</strong></li>
<li><strong>Il valorise vos r&eacute;alisations, services et informations diverses.</strong></li>
<li><strong>Il refl&egrave;te une image positive et professionnelle de votre entreprise.&nbsp;</strong></li>
<li><strong>Il augmente votre VISIBILIT&Eacute;, vos CLIENTS POTENTIELS et donc votre CHIFFRE D'AFFAIRES.&nbsp;</strong></li>
</ul>
<p>Je me permets de vous contacter aujourd'hui afin de vous accompagner dans l'&eacute;laboration de votre site internet.</p>
<p>Je suis&nbsp;<strong>Webmaster</strong>&nbsp;sp&eacute;cialis&eacute; dans la&nbsp;<strong>cr&eacute;ation de sites internet pour les TPE/PME et les ind&eacute;pendants</strong>.</p>
<p>Je vous fournis,&nbsp;<strong>cl&eacute; en main</strong>, une pr&eacute;sence sur le Web en quelques jours !&nbsp;<em>(Voir pi&egrave;ce jointe n&deg;1)&nbsp;</em></p>
<p>Vous pouvez voir ci-joint quelques exemples de sites.<strong>&nbsp;</strong><em>(Voir pi&egrave;ce jointe n&deg;2) </em></p>
<p>&nbsp;</p>
<p>Je suis &agrave; votre disposition pour &eacute;changer avec vous, si vous souhaitez en savoir plus sur mes solutions.</p>
<p>&nbsp;</p>
<p>En vous souhaitant une bonne journ&eacute;e.</p>
<p>Bien cordialement,&nbsp;</p>
""" + f'<tbody><tr><td valign="top" width="100" style="vertical-align: top; --darkreader-inline-outline:#b30000;" title=""><img src="{signatureImagePath}" width="96" height="63" class="CToWUd"></td><td valign="top" style="font-size:1em;padding:0px 0px 0px 15px;vertical-align:top"><table cellspacing="0" cellpadding="0" border="0" style="border-spacing: 0px; border-collapse: collapse; width: 385px; max-width: 400px; line-height: 1.4; font-family: Georgia, serif; font-size: 14.04px; color: rgb(0, 0, 1); --darkreader-inline-color:#e8e6e3;" data-darkreader-inline-color=""><tbody><tr><td style="padding-bottom:4px"><div style="font-family:Georgia,serif"><span style="font-size: 1.2em; color: rgb(42, 42, 42); font-weight: 600; --darkreader-inline-color:#cdc9c3;" data-darkreader-inline-color="">Alexis Sevrin</span><font style="vertical-align:inherit"><font style="vertical-align:inherit">&nbsp;|&nbsp;</font><font style="vertical-align:inherit"><b>Webmaster</b><br></font></font></div></td></tr><tr><td style="padding:1px 0px"><div style="font-family:Georgia,serif"><font style="vertical-align:inherit">|&nbsp;</font><span style="font-weight: 600; color: rgb(42, 42, 42); --darkreader-inline-color:#cdc9c3;" data-darkreader-inline-color="">téléphone:&nbsp;&nbsp;</span>06 25 30 57 11</div></td></tr><tr><td style="padding:1px 0px"><div style="font-family:Georgia,serif"><font style="vertical-align:inherit">|&nbsp;</font><span style="font-weight: 600; color: rgb(42, 42, 42); --darkreader-inline-color:#cdc9c3;" data-darkreader-inline-color="">courriel:&nbsp;&nbsp;</span><a href="mailto:alexissevrin.web@gmail.com" style="color: rgb(0, 0, 1); --darkreader-inline-color:#e8e6e3;" target="_blank" data-darkreader-inline-color="">alexissevrin.web@<wbr>gmail.com</a></div></td></tr></tbody></table></td></tr></tbody></p>'

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
            attach_part.add_header("Content-Disposition", "attachment", filename=file)
            msg.attach(attach_part)
    return msg


def send_mail(email, password, FROM, TO, msg, rowNb):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()

    print('Sent...')
    # print(f'Envoi du mail a {TO}')
    # print('\n' + msg.as_string())

    with open('log.txt', 'w+') as file:
        file.write(f'Mail envoyé au clients de la ligne {startingRow} à la ligne {rowNb}')
        file.close()

def makeRtf(client):


    sexe = client['sex']
    nom = client['nom']
    ville = client['ville']

    file = f'{sexe}-{nom}-{ville}.rtf'
    out_file = open(r'rtfs\\'+file, 'w')

    text = """{\\rtf1 {\\fonttbl {\\f0 Arial;}}
\\b Objet: \\b0\line
""" + sexe + '.' + nom + """, vos clients vous cherchent sur internet !\line
\line
\\b Mail : \\b0\line
""" + sexe + '.' + nom + """,\line
\line
\\b Félicitations pour la création de votre entreprise !\\b0\line
Lorsque l'on décide d'ouvrir son affaire, il est important de penser à sa visibilité.\line
Chaque jour, plus de \\b 6,9 milliards de personnes \\b0 recherchent \\b un service sur Google.\\b0\line
Imaginez le potentiel commercial qui s'y cache à \\b """ + ville + """ !\line
\line
85% des internautes contactent un professionnel via le web !\\b0\line
Aujourd'hui, il est donc essentiel d'avoir un site internet pour améliorer son image et ses performances commerciales.\line
\line
Vos concurrents l'ont compris, et \\b absorbent vos clients potentiels \\b0 grâce à leur site internet.\line
\line
\\ul Créer son propre site génère énormément d'avantages, c'est votre carte de visite digitale :\\ul0\line
\line \\b
    •	Votre site internet est ouvert 24h/24 et 7j/7 !\line
    •	Il remplace vos documents publicitaires et réduit vos coûts marketing.\line
    •	Il valorise vos réalisations, services et informations diverses.\line
    •	Il reflète une image positive et professionnelle de votre entreprise.\line
    •	Il augmente votre VISIBILITÉ, vos CLIENTS POTENTIELS et donc votre CHIFFRE D'AFFAIRES. \\b0\line
\line
Je me permets de vous contacter aujourd'hui afin de vous accompagner dans l'élaboration de votre site internet.\line
Je suis \\b Webmaster \\b0 spécialisé dans la \\b création de sites internet pour les TPE/PME et les indépendants \\b0\line
Je vous fournis, \\b clé en main \\b0, une présence sur le Web en quelques jours ! (Voir pièce jointe n°1)\line
Vous pouvez voir ci-joint quelques exemples de sites. (Voir pièce jointe n°2)\line
\line
Je suis à votre disposition pour échanger avec vous, si vous souhaitez en savoir plus sur mes solutions.\line
\line
En vous souhaitant une bonne journée.\line
\line
Bien cordialement,\line
\line
Alexis Sevrin\line
Webmaster Freelance\line
}"""

    out_file.write(text)

sg.theme('Dark')
layout = [
    [sg.Text('Fichier .xls à utiliser: '), sg.InputText(size=(65,1),key=('excelPath')), sg.FileBrowse(size=(10,1))],
    [sg.Text('_' * 99)],
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
startingRow = None



clientSex   = None
clientNom   = None
clientVille = None
clientMail  = None
clientRow = None

wb = None
sheet = None
excelPath = None


while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Quitter":
        break




    if event == 'sendMail':
        excelPath = values['excelPath']
        wb = xlrd.open_workbook(excelPath)
        sheet = wb.sheet_by_index(0)

        sendingMail = True
        delay = values['delai']
        endTime = int(time.time()) + int(delay)
        clientList = getInfos()
        startingRow = clientList[0]['rowNb']

        window.Element('sex').Update(clientList[0]['sex'])
        window.Element('name').Update(clientList[0]['nom'])
        window.Element('city').Update(clientList[0]['ville'])
        window.Element('mail').Update(clientList[0]['mail'])

        print(f'Starting in {delay}s...')

    if event == 'word':

        excelPath = values['excelPath']
        wb = xlrd.open_workbook(excelPath)
        sheet = wb.sheet_by_index(0)

        clientList = getInfos()
        print('Création des .rtf en cours, cela peut prendre un peu de temps...')
        try:
            os.mkdir('rtfs')
        except:
            None
        for client in clientList:
            makeRtf(client)
        print('Création des .rtf: Finalisée !')

    nowTime = int(time.time())
    while sendingMail:
        event,values = window.read(100)
        nowTime = int(time.time())
        if nowTime > endTime:
            client = clientList[clientNumber]





            msg = makeMail(client)
            send_mail(creds[0], creds[1], creds[0], client['mail'], msg, client['rowNb'])
            endTime = int(time.time())+int(delay)
            clientNumber+=1

            clientRow = clientList[clientNumber]['rowNb']
            window.Element('sex').Update(clientList[clientNumber]['sex'])
            window.Element('name').Update(clientList[clientNumber]['nom'])
            window.Element('city').Update(clientList[clientNumber]['ville'])
            window.Element('mail').Update(clientList[clientNumber]['mail'])

        if event == 'stopMail':
            sendingMail = False
            print("Stop...")
            window.Element('sex').Update('')
            window.Element('name').Update('')
            window.Element('city').Update('')
            window.Element('mail').Update('')
            with open('log.txt', 'w+') as file:
                file.write(f'Mail envoyé au clients de la ligne {startingRow} à la ligne {clientRow-1}')
                file.close()

        if event == 'confirm':
            clientList[clientNumber]['sex'] = values['sex']
            clientList[clientNumber]['nom'] = values['name']
            clientList[clientNumber]['ville'] = values['city']
            clientList[clientNumber]['mail'] = values['mail']


# clientList = getInfos()
# autoMode()
