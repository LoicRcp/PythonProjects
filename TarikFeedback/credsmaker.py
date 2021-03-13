import pickle

botToken = input("Entrez le bot_token: ")

with open("creds.pickle", "wb") as file:
    pickle.dump(botToken, file)

input('Press a key to exit')