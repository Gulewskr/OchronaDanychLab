def new_key(key):
    key_length = len(key)
    for i in range(0, key_length):
        index = key_length - i - 1
        code = ord(key[index])
        if(code < 122):
            key[index] = chr(code + 1)
            return key
        else:
            key[index] = 'a'
    return key

import base64
import math
from arc4 import ARC4

file = open("encrypted.3rc4", "rb")
s = file.read()

key=list("aaa")
entropy = 8
min_entropy = entropy
min_entropy_key = ""
original_text = ""
entropy_cap = 5.2

while(entropy >= entropy_cap):
    entropy = 0
    arc4 = ARC4(''.join(key))
    cipher = arc4.decrypt(s)
    cipher = arc4.decrypt(cipher)
    cipher = arc4.decrypt(cipher)
    occurencies = [None] * 256
    for i in range(256):
        occurencies[i] = 0
    for b in cipher:
        occurencies[b] = occurencies[b] + 1
    for i in range(256):
        probability = occurencies[i] / len(cipher)
        if ( probability > 0):
            entropy = entropy - probability * math.log ( probability, 2 )
    if(entropy < min_entropy):
        min_entropy = entropy
        min_entropy_key = key
        original_text = cipher
    if((''.join(key))=="zzz" or entropy < entropy_cap):
        break
    key = new_key(key)

print("klucz: ", min_entropy_key)
print("entropia:", min_entropy)
print(original_text.decode("utf-8"))
file.close()