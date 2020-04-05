import requests
import hashlib
import sys

def check_pass(hash):
    req_url = f'https://api.pwnedpasswords.com/range/{hash[:5]}'
    res = requests.get(req_url)
    if res.status_code != 200:
       raise RuntimeError(f'Error: {res.status_code}, check the API')
    return get_leaks(res, hash[5:])

def get_leaks(hashes, hash):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, c in hashes:
        if h == hash:
            return c
    return 0
    
def hasher(paswd):
    hashed_pass = hashlib.sha1(paswd.encode('utf-8')).hexdigest().upper()
    return check_pass(hashed_pass) 

def main():
    with open('./passwords.txt', 'r') as file:
        passwords = file.read().splitlines()  
    for password in passwords:
        result = hasher(password)
        if result:
            print(f'The password {password} is pwned {result} times, it is better to change it')
        else:
            print('The password is secure')
    
if __name__ == '__main__':
    main()
