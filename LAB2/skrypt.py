from arc4 import ARC4
import re
import math

WANTED_ENTROPY = 5
INPUT_FILE = 'encrypted.3rc4' # encrypted.3rc4 crypto.rc4 crypto2.rc4
OUTPUT_FILE_WRITE = True

f = open(INPUT_FILE, 'rb').read()
fw = open('decrypted', 'w')

def Licz_p(str):
    freq = {}
    for i in str:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
    p = []
    for i in freq:
        p.append(freq[i]/len(str))
    return p

def Licz_Entropie(p):
    res = 0
    for i in p:
        res += i * math.log2(i)
    return -res

alfabet = "abcdefghijklmnopqrstuvwxyz"
for i in range(len(alfabet)):
    for j in range(len(alfabet)):
        for k in range(len(alfabet)):
            key = alfabet[i] + alfabet[j] + alfabet[k]
            text = ARC4(key).decrypt(f)
            p = Licz_p(text)
            res = Licz_Entropie(p)
            if(res < WANTED_ENTROPY):
                print("Dla klucza: ", key, "  entropia wynosi: ", res)
                print("Zdekodowany tekst")
                print(text)
                if(OUTPUT_FILE_WRITE):
                    fw.write("Zdekodowany tekst klucz '" + str(key) + "':")
                    fw.write('\n')
                    fw.write(text.decode("utf-8"))
    print("sprawdzono klucze ",  alfabet[i],  "**")
