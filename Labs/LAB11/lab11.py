import multiprocessing
import time
import ctypes

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

def xor64(a, b):
    block = bytearray(a)
    for j in range(8):
        block[j] = a[j] ^ b[j]
    return block

def encryptMapper(i):
    nonce = bytes(key, "utf8")
    counter = bytes(i);
    offset = i*block_size
    block = bytes(shared_data[offset:offset+block_size])
    for j in range(10000):
        block = des.encrypt(block)
    encrypted = bytes(xor64(block, nonce+counter))     
    output_data[offset:offset+block_size] = bytearray(encrypted)
    return i   

def decryptMapper(i):
    nonce = bytes(key, "utf8")
    counter = bytes(i);
    offset = i*block_size
    block = bytes(output_data[offset:offset+block_size])
    for j in range(10000):
        block = des.encrypt(block)
    encrypted = bytes(xor64(block, nonce+counter))     
    shared_data[offset:offset+block_size] = bytearray(encrypted)
    return i   


plain_text = "alamakot"*10
plain_text = bytes(plain_text, "utf8")
key = "haslo123"
iv = get_random_bytes(8)
iv = b'\x00'*8
block_size = 8
no_blocks = int(len(plain_text)/block_size)

des = DES.new(key.encode("utf8"), nonce=b'', initial_value=iv,mode=DES.MODE_CTR)

shared_data = multiprocessing.RawArray(ctypes.c_ubyte, plain_text)
output_data = multiprocessing.RawArray(ctypes.c_ubyte, plain_text)

print("before");
print(bytes(shared_data));

#multiprocessing.freeze_support()
pool = multiprocessing.Pool(4)
starttime = time.time()
pool.map(encryptMapper, range(no_blocks))
# print('CTR encrypt time parallel: ', (time.time() - starttime))

decrypted = bytes(output_data)
print("after")
print(decrypted)
shared_data = multiprocessing.RawArray(ctypes.c_ubyte, plain_text)
pool.map(decryptMapper, range(no_blocks))
encrypted = bytes(shared_data)
print("encrypted")
print(encrypted)