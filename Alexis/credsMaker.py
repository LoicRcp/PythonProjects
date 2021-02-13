import pickle

login = input("Gmail login: ")
password = input("Gmail password: ")

with open('creds.pickle','wb') as creds:
    pickle.dump([login,password], creds)
