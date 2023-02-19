from math import ceil
import base64
import os
from random import randint
from sys import prefix
from Crypto.Cipher import AES
from numpy import block
from utils import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
backend = default_backend()


def split_bytes_in_blocks(x, block_size):
    nb_blocks = ceil(len(x)/block_size)
    return [x[block_size*i:block_size*(i+1)] for i in range(nb_blocks)]


def pkcs7_padding(message, block_size):
    padding_length = block_size - (len(message) % block_size)
    if padding_length == 0:
        padding_length = block_size
    padding = bytes([padding_length]) * padding_length
    return message + padding


def pkcs7_strip(data):
    padding_length = data[-1]
    return data[:- padding_length]


def encrypt_aes_128_ecb(msg, key):
    padded_msg = pkcs7_padding(msg, block_size=16)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    return encryptor.update(padded_msg) + encryptor.finalize()


def decrypt_aes_128_ecb(ctxt, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ctxt) + decryptor.finalize()
    message = pkcs7_strip(decrypted_data)
    return message

# You are not suppose to see this
class Oracle:
    def __init__(self):
        self.key = 'Mambo NumberFive'.encode()
        self.prefix = 'PREF'.encode()
        self.target = base64.b64decode(  # You are suppose to break this
            "RG8gbm90IGxheSB1cCBmb3IgeW91cnNlbHZlcyB0cmVhc3VyZXMgb24gZWFydGgsIHdoZXJlIG1vdGggYW5kIHJ1c3QgZGVzdHJveSBhbmQgd2hlcmUgdGhpZXZlcyBicmVhayBpbiBhbmQgc3RlYWwsCmJ1dCBsYXkgdXAgZm9yIHlvdXJzZWx2ZXMgdHJlYXN1cmVzIGluIGhlYXZlbiwgd2hlcmUgbmVpdGhlciBtb3RoIG5vciBydXN0IGRlc3Ryb3lzIGFuZCB3aGVyZSB0aGlldmVzIGRvIG5vdCBicmVhayBpbiBhbmQgc3RlYWwuCkZvciB3aGVyZSB5b3VyIHRyZWFzdXJlIGlzLCB0aGVyZSB5b3VyIGhlYXJ0IHdpbGwgYmUgYWxzby4="
        )

    def encrypt(self, message):
        return encrypt_aes_128_ecb(
            self.prefix + message + self.target,
            self.key
        )

# Task 1
def findBlockSize():
    initialLength = len(Oracle().encrypt(b''))
    i = 0
    prev_len = len(Oracle().encrypt(b'X'))
    while 1:  # Feed identical bytes of your-string to the function 1 at a time until you get the block length
        # You will also need to determine here the size of fixed prefix + target + pad
        # And the minimum size of the plaintext to make a new block
        length = len(Oracle().encrypt(b'X'*i))

        if (prev_len != length):
            block_size = length - prev_len
            minimumSizeToAlighPlaintext = i - 1
            sizeOfTheFixedPrefixPlusTarget = initialLength
            return block_size, sizeOfTheFixedPrefixPlusTarget, minimumSizeToAlighPlaintext
        
        i += 1

# Task 2
def findPrefixSize(block_size):
    # Find the situation where prefix_size + padding_size - 1 = block_size
    # Use split_bytes_in_blocks to get blocks of size(block_size)
    c0 = split_bytes_in_blocks(Oracle().encrypt(b''), block_size)
    c1 = split_bytes_in_blocks(Oracle().encrypt(b'X'), block_size)
    first_diff_block = 0
    for i in range(0, len(c0)):
        if c0[i] != c1[i]:
            first_diff_block = i
            break

    previous_blocks = c0
    i = 1
    while 1:
        c = split_bytes_in_blocks(Oracle().encrypt(b'X'*i), block_size)
        if c[first_diff_block] == previous_blocks[first_diff_block]:
            return block_size - i + 1
        i += 1
        previous_blocks = c


# Task 3
def recoverOneByteAtATime(block_size, prefix_size, target_size):
    known_target_bytes = b""
    # aflu primele 12 caractere
    for _ in range(block_size - prefix_size):
            known_len = len(known_target_bytes)
            padding_length = (- known_len - 1 - prefix_size) % block_size
            padding = b"X" * padding_length
            c = split_bytes_in_blocks(Oracle().encrypt(padding), block_size)
            for i in range(0, 255):
                guess = chr(i).encode()
                c_guess = split_bytes_in_blocks(Oracle().encrypt(padding + known_target_bytes + guess), block_size)
                if c_guess[0] == c[0]:
                    known_target_bytes += guess
                    break

    # aflu urmatoarele 3 caractere ca sa am 15 cunoscute in total sa pot
    # afla urmatorul block
    block_minus_prefix_size = block_size - prefix_size
    for i in range(prefix_size - 1):
        padding = b"X" * (block_minus_prefix_size + (prefix_size - 1 - i))
        c = split_bytes_in_blocks(Oracle().encrypt(padding), block_size)
        for i in range(0, 255):
            guess = chr(i).encode()
            c_guess = split_bytes_in_blocks(Oracle().encrypt(padding + known_target_bytes + guess), block_size)
            if c_guess[1] == c[1]:
                known_target_bytes += guess
                break

    # folosind cele 15 cunoscute aflu urmatoarele 12 caractere
    fixed_padding = b"X" * block_minus_prefix_size
    for i in range(block_minus_prefix_size):
        padding = b"X" * (block_minus_prefix_size - i)
        c = split_bytes_in_blocks(Oracle().encrypt(padding), block_size)
        for i in range(0, 255):
            guess = chr(i).encode()
            last_known_target_bytes = known_target_bytes[-15:]
            c_guess = split_bytes_in_blocks(Oracle().encrypt(fixed_padding + last_known_target_bytes + guess), block_size)
            if c_guess[1] == c[1]:
                known_target_bytes += guess
                break

    # acum pot afla cate un block la fiecare iteratie
    # pentru ca stiu ultimele 15 caractere si de asemenea am 12 caractere
    # ca buffer pentru a-mi umple block_size - prefix_size pozitii
    for curr_block_index in range((target_size // block_size) + 2):
        for i in range(block_size):
            padding = b"X" * (block_size - i)
            c = split_bytes_in_blocks(Oracle().encrypt(padding), block_size)
            for i in range(0, 255):
                guess = chr(i).encode()
                last_known_target_bytes = known_target_bytes[-15:]
                c_guess = split_bytes_in_blocks(Oracle().encrypt(fixed_padding + last_known_target_bytes + guess), block_size)
                if c_guess[1] == c[curr_block_index]:
                    known_target_bytes += guess
                    break

    print(known_target_bytes.decode())

# Find block size, prefix size, and length of plaintext size to allign blocks
block_size, sizeOfPrefixTargetPadding, minimumSizeToAlignPlaintext = findBlockSize()
print("Block size:\t\t\t\t" + str(block_size))
print("Size of prefix, target, and padding:\t" + str(sizeOfPrefixTargetPadding))
print("Pad needed to align:\t\t\t" + str(minimumSizeToAlignPlaintext))

# Find size of the prefix
prefix_size = findPrefixSize(block_size)
print("\nPrefix Size:\t" + str(prefix_size))

# # Size of the target
target_size = sizeOfPrefixTargetPadding - \
     minimumSizeToAlignPlaintext - prefix_size

print(target_size)

print("\nTarget:")
recoverOneByteAtATime(block_size, prefix_size, target_size)