from passlib.hash import des_crypt
import string
import random
import time

passwords3 = ["abc", "SdW", "ZZZ", "bSd", "hIA"]
salt = ''.join(random.sample(string.ascii_letters, 2))

for m in passwords3:
    passwd = des_crypt.hash( m, salt=salt)
    print(m, " -> ", passwd)
    chars = string.ascii_letters
    start = time.time()
    for a in chars:
        for b in chars:
            for c in chars:
                trial = a+b+c
                crypted = des_crypt.hash( trial, salt=salt )
                if crypted == passwd:
                        end = time.time()
                        break
            if crypted == passwd:
                break
        if crypted == passwd:
            break
    if crypted == passwd:
        print( "Hasło złamane: " + trial)
        print("czas ", end - start)
    else:
        print( "Nie złamano hasła" )

'''
Wyniki:
3-znakowe hasło:
    -wszystkie możliwości: 74088 - 329 sekund
    -średnio: 120 sekund
Szacowania:
4-znakowe hasło:
    -wszystkie możliwości: 3111696 ~ 3.83 godziny
    -średnio: 1.39 godziny
5-znakowe hasło:
    -wszystkie możliwości: 130691232 ~ 161.21 godziny
    -średnio: 58.8 godziny
6-znakowe hasło:
    -wszystkie możliwości: 5489031744 ~ 282.12 dni
    -średnio: 103 dni
'''