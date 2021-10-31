from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

def prepareinput(str, bl):
    return str

def encryptWithAESCBC(str, passwd):
    key = PBKDF2(passwd, b"salt")
    iv = get_random_bytes(16)
    print("wygenerowany klucz z hasla: ", key)
    str = prepareinput(str, 16)
    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted = aes.encrypt(str)
    return (encrypted, key, iv)

def decryptWithAESCBC(str, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    decrypted = aes.decrypt(str)
    return decrypted



wejscie = input("Podaj halso: ")

#wczytanie pliku i przygo
data = str.encode("Tekst do zaszyfrowania0000000000")

(e, k, i) = encryptWithAESCBC( data, wejscie)
print("zaszyfrowany tekst: \n",  e)
d = decryptWithAESCBC(e, k, i)
print("odszyfrowany tekst: \n",d)