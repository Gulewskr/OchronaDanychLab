import sys
import random

def trivial_hash(dane):
        hash = 0
        for znak in dane:
                hash += ord(znak)
        return hash % 999


if(len(sys.argv) > 1):
    password = sys.argv[1]
else:
    password = "password"

protected_password = trivial_hash(password)
print( "hash dla hasła: ", password, " = ", protected_password )

mypassword = ""
myhash = trivial_hash(mypassword)

while(myhash != protected_password):
    #zestaw białych znaków z c
    r = random.randint(1, 6)
    if(r == 1):
        mypassword += ' '
    if(r == 2):
        mypassword += '\t'
    if(r == 3):
        mypassword += '\n'
    if(r == 4):
        mypassword += '\v'
    if(r == 5):
        mypassword += '\f'
    if(r == 6):
        mypassword += '\r'
    myhash = trivial_hash(mypassword)

print( "znaleziony hash", myhash )
print( "użyte hasło: \n", mypassword )