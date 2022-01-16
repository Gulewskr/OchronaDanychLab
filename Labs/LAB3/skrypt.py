from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

def prepareinput(_str, bl):
    _str = str.encode(_str, "utf-8")
    r = bl - len(_str) % bl
    if(r != 0):
        _str = bytearray(_str)
        for i in range(r):
            _str.append(r)
    return _str

def encryptWithAESCBC(_str, passwd):
    key = PBKDF2(passwd, b"salt")
    iv = get_random_bytes(16)
    print("wygenerowany klucz z hasla: ", key)
    print("wygenerowany wartość iniciująca: ", iv)
    _str = prepareinput(_str, 16)
    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted = aes.encrypt(_str)
    return (encrypted, key, iv)

def decryptWithAESCBC(str, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    decrypted = aes.decrypt(str)
    return decrypted


wejscie = input("Podaj halso: ")
in_file = input("Podaj nazwę pliku do zaszyfrowania: ")

#data = "Tekst do zaszyfrowania"
data = open(in_file, 'r').read()


of = open('encrypted', 'wb')
(e, k, i) = encryptWithAESCBC( data, wejscie)
print("\n ---- ZASZYFROWANIE ----")
print("zaszyfrowany tekst: \n",  e)
of.write(e)
of.close()

print("\n ---- ODSZYFROWANIE ----")
d = decryptWithAESCBC(e, k, i)
print("odszyfrowany tekst: \n",d)