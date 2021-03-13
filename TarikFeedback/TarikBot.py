import pickle



try:
    with open('creds.pickle', 'rb') as credsFile:
        botToken = pickle.load(credsFile)

except:
    print("No creds file in the folder...")
    exit()