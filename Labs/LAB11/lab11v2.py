import multiprocessing
import time
import ctypes

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter

#times = 10000
#DES.block_size = 64Bit
ctrEncrypt = Counter.new(DES.block_size)
ctrDecrypt = Counter.new(DES.block_size)

def xor(text, encrypt):
    block = bytearray(text)
    for j in range(len(block)):
        block[j] = text[j] ^ encrypt[j]
    return block

def encrypt_CTR(key, plain_text):
    vector = bytearray(plain_text)
    des = DES.new(key, DES.MODE_CTR, counter = ctrEncrypt)
    for i in range(blocksNumber):
        offset = i*DES.block_size
        plain_text_block = plain_text[offset:offset+DES.block_size]
        enc_key = des.encrypt(ctrEncrypt)
        encrypted = bytes(xor(plain_text_block, enc_key))
        vector[offset:offset+DES.block_size] = bytearray(encrypted)
        iv = encrypted
    return bytes(vector)        

def decrypt_CBC_serial(key, encrypted, iv):
    vector = bytearray(encrypted)
    des = DES.new(key, DES.MODE_CTR, counter = ctrDecrypt)
    for i in range(no_blocks):
        offset = i*block_size
        block = encrypted[offset:offset+block_size]
        intermediate = block
        for j in range(times):
           intermediate = des.decrypt(intermediate)
        decrypted = bytes(xor64(intermediate, iv))
        vector[offset:offset+block_size] = bytearray(decrypted)
        iv = block
    return bytes(vector)        


plain_text = "alamakot"*1000
plain_text = bytes(plain_text, "utf8")
key = "haslo123" #64Bit
iv = get_random_bytes(8)
#iv = b'\x00'*8
#block_size = 8
blocksNumber = int(len(plain_text)/8)

starttime = time.time()
encryptedCBC = encrypt_CBC_serial(key, plain_text, iv)
print('CBC Encrypt time serial: ', (time.time() - starttime))
print("Encrypted CBC: ", encryptedCBC)

starttime = time.time()
decryptedCBC = decrypt_CBC_serial(key, encryptedCBC, iv)
print('CBC Decrypt time serial: ', (time.time() - starttime))
print("Decrypted CBC: ", decryptedCBC)

def mapper(i):
    offset = i*block_size
    block = bytes(shared_data[offset:offset+block_size])
    for j in range(times):
        block = des.decrypt(block)
    if i==0: 
        previous_block = iv
    else:
        previous_block = bytes(shared_data[offset-block_size:offset])
    decrypted = bytes(xor64(block, previous_block))     
    output_data[offset:offset+block_size] = bytearray(decrypted)
    return i

des = DES.new(key, DES.MODE_CTR, counter = ctrDecrypt)
shared_data = multiprocessing.RawArray(ctypes.c_ubyte, encryptedCBC)
output_data = multiprocessing.RawArray(ctypes.c_ubyte, encryptedCBC)
pool = multiprocessing.Pool(16)
starttime = time.time()
pool.map(mapper, range(no_blocks))
print('CBC Decrypt time parallel: ', (time.time() - starttime))
decrypted = bytes(output_data)
#print(decrypted)