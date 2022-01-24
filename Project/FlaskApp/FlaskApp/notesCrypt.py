#Szyfrowanie i odszyfrowywanie notatek
from Crypto.Cipher import AES
from .config import Config

def encryptNote(note):
    cipher = AES.new(Config.NOTEKEY, AES.MODE_CFB, Config.NOTEKIV)
    _note = bytearray(note, "utf-8")
    return cipher.encrypt(_note)

def decryptNote(note):
    cipher = AES.new(Config.NOTEKEY, AES.MODE_CFB, Config.NOTEKIV)
    return cipher.decrypt(note).decode()