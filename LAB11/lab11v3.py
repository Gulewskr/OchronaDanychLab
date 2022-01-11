from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter


def addPadding(data):
        padding = len(data) % 64
        data + b'\x00'*padding;
        return data

def encrypt_CTR(text, key, ctr):
    text = addPadding(text)
    cipher = DES.new(key, DES.MODE_CTR, counter=ctr)
    result = cipher.encrypt(text)
    return result

def decrypt_CTR(text, key, ctr):
    text = addPadding(text)
    cipher = DES.new(key, DES.MODE_CTR, counter=ctr)
    result = cipher.decrypt(text)
    return result

#---------------------------------------------------------------
block_size = DES.block_size*8
plaintext = bytearray( "ala ma kota a ja mam psa" * 100, "utf8")

key = get_random_bytes(8)
nonce = get_random_bytes(4)

ctrEnc = Counter.new(block_size)
ctrDec = Counter.new(block_size)

print("Przed szyfrowaniem")
print(plaintext)

encrypted = encrypt_CTR(plaintext, key, ctrEnc)
print("Po zaszyfrowaniu")
print(encrypted)


decrypted = decrypt_CTR(encrypted, key, ctrDec)
print("Po odszyfrowaniu")
print(decrypted)