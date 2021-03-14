import pickle

print("Ce programme permet de générer un fichier permettant une sécurisée avec l'api Telegram\n"
      "L'API id et l'API hash s'obtiennent sur une page particulière de Telegram\n"
      "Le numéro de téléphone s'écrit au format internationnal: +33 6 12 34 56 78\n"
      "Le botToken s'obtient en allant parler au BotFather\n"
      "Si votre numéro est français, il faut mettre +33 devant et omettre le premier 0")


api_id = input("Api_id: ")
api_hash = input("Api_hash: ")
botToken = input("Bot_Token: ")
phoneNb = input("phoneNb: +")
phoneNb = "+" + phoneNb

creds = [api_id, api_hash, phoneNb, botToken]
with open("creds.pickle", "wb") as file:
    pickle.dump(creds, file)

input('Press a key to exit')