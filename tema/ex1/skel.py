from pwn import *
import base64 as b64
from time import sleep
from secretz import *

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

LOCAL = False  # Local means that you run binary directly

if LOCAL:
    # Complete this if you want to test locally
    r = process("./server.py")
else:
    r = remote("141.85.224.117", 1337)  # Complete this if changed

def read_options():
    """Reads server options menu."""
    r.readuntil(b"Input:")

def get_token():
    """Gets anonymous token as bytearray."""
    read_options()
    r.sendline(b"1")
    token = r.readline()[:-1]
    return b64.b64decode(token)

def login(tag):
    """Expects bytearray. Sends base64 tag."""
    r.readline()
    read_options()
    r.sendline(b"2")
    # sleep(0.01) # Uncoment this if server rate-limits you too hard
    r.sendline(b64.b64encode(tag))
    r.readuntil(b"Token:")
    response = r.readline().strip()
    return response

token = get_token()
secret_len = INTEGRITY_LEN + len(SERVER_PUBLIC_BANNER)
cipher, secret = token[:-secret_len], token[-secret_len:-INTEGRITY_LEN]
guest_name = b"Anonymous"
rnd = byte_xor(guest_name, cipher)
secret_plain = b"Ephvuln"
my_cipher = byte_xor(secret_plain, rnd)
for tag in range(256):
    tag_hex = tag.to_bytes(1, 'little')
    payload = my_cipher + secret + tag_hex
    response = login(payload).decode('utf-8')
    if "CTF" in response:
        print("[*] Found flag:",response)

r.close()