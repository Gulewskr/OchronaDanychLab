from math import sqrt
import random
from Crypto.PublicKey import RSA
'''
def isPrime(num):
    if num > 1:
        for i in range(2, int(num/2)+1):
            if (num % i) == 0:
                return False
        return True
    else:
        return False

Wynik:
Czy p jest liczbą pierwszą
12284053695168772318265120651541871640797648269853548902745970503928999543243367802772249512315637982642154651611423977832425066562939122820170432544136269     jest liczbą pierwszą
Czy q jest liczbą pierwszą
12338720626105269865944674170159697259773215128846196848842066192362451135229635449532758902080179695788554307055391851884293897855804588063391652809939017     jest liczbą pierwszą
63541   jest liczbą pierwszą
41479   jest liczbą pierwszą
Znalezione p i q dla n: 2635617139  p: 41479  q: 63541.0
'''

def isPrimeFermatTest(num, tryNum):
    i = 0
    while i < tryNum:
        a = random.randint(1, num - 1)
        if pow(a, (num - 1), num) == 1:
            i = i + 1
        else:
            return False
    return True

def isPrimeToString(num, func):
    if func(num, 1000):
        return str(num) + "\tjest liczbą pierwszą"
    else:
        return str(num) + "\tnie jest liczbą pierwszą"

def factorizeEnumerate(key, num, func):
    for i in range(num, 100, -1):
        if func(i, 10000):
            q = key / i
            if(q % 1 == 0):
                if func(int(q), 10000):
                    return (i, q)
    return (None, None)

def factorizeUsingSito(key, sito):
    for p in sito:
        q = key / p
        if(q in sito):
            return (p, q)
    return (None, None)

r = RSA.generate(1024)
print("Czy p jest liczbą pierwszą")
print(isPrimeToString(r.p, isPrimeFermatTest))
print("Czy q jest liczbą pierwszą")
print(isPrimeToString(r.q, isPrimeFermatTest))

#liczby wygenerowane generatorem https://asecuritysite.com/encryption/random3
p = [63541,      1206940723,            12583678837591311509]
q = [41479,      439222151,             17217929697796648003]
t = [2635617139, 530115100485555173,    216664897565298644996349462416795766527]

for n in t:
    (p, q) = factorizeEnumerate(n, int(sqrt(n)), isPrimeFermatTest)
    if(p != None):
        print("Znalezione p i q dla n:", n," p:", p, " q:", q)
    else:
        print("Nie znaleziono rozwiązania dla n:", n)