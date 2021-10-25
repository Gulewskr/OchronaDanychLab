from arc4 import ARC4
import re
import math

'''
Znalezione klucze
crypto2.rc4 -> eac - 4.2885559405989095
crypto.rc4 -> def - 4.455746513165591
encrypted.3rc4 -> abc - 5.0704283662168725
'''


WANTED_ENTROPY = 5.5
INPUT_FILE = 'encrypted.3rc4' # encrypted.3rc4 crypto.rc4 crypto2.rc4
OUTPUT_FILE_WRITE = True

f = open(INPUT_FILE, 'rb').read()
fw = open('decrypted', 'w')

foundEntropy = 8
foundKey = "key"

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
            a = ARC4(key)
            text = a.decrypt(f)
            text = a.decrypt(text)
            text = a.decrypt(text)
            p = Licz_p(text)
            res = Licz_Entropie(p)
            if(res < foundEntropy):
                foundEntropy = res
                foundKey = key
            if(res < WANTED_ENTROPY):
                print("Dla klucza: ", key, "  entropia wynosi: ", res)
                print("Zdekodowany tekst")
                print(text.decode("utf-8"))
                if(OUTPUT_FILE_WRITE):
                    fw.write("Zdekodowany tekst klucz '" + str(key) + "':")
                    fw.write('\n')
                    fw.write(text.decode("utf-8"))
                exit()
    print("sprawdzono klucze ",  alfabet[i],  "**")

print("Sprawdzono wszystkie klucze najniższa entropia dla klucza ", foundKey, " wynosi ", foundEntropy)
a = ARC4(foundKey)
text = a.decrypt(f)
text = a.decrypt(text)
text = a.decrypt(text)
print("tekst: ")
print(text)