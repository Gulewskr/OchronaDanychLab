from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

def prepareinput(_str, bl):
    r = bl - len(_str) % bl
    if(r != 0):
        for i in range(r):
            _str = _str + "0"
    return _str

def encryptWithAESCBC(_str, passwd):
    key = PBKDF2(passwd, b"salt")
    iv = get_random_bytes(16)
    print("wygenerowany klucz z hasla: ", key)
    _str = prepareinput(_str, 16)
    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted = aes.encrypt(str.encode(_str))
    return (encrypted, key, iv)

def decryptWithAESCBC(str, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    decrypted = aes.decrypt(str)
    return decrypted


wejscie = input("Podaj halso: ")
data = "Tekst do zaszyfrowania"

(e, k, i) = encryptWithAESCBC( data, wejscie)
print("zaszyfrowany tekst: \n",  e)
d = decryptWithAESCBC(e, k, i)
print("odszyfrowany tekst: \n",d)