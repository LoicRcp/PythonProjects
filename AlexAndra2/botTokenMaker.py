import pickle

botToken = input("Rentrez le botToken: ")
fileName = input("\nEntrez le nom du fichier (botTokenFileActive pour être celui utilisé par le bot): ")

with open(str(fileName)+ ".pickle","wb") as tokenFile:
    pickle.dump(botToken,tokenFile)