from utils import *
from operator import itemgetter
import bisect
from Crypto.Cipher import DES


def get_index(a, x):
    """Locate the leftmost value exactly equal to x in list a"""
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return -1


def des_enc(k, m):
    """
    Encrypt a message m with a key k using DES as follows:
    c = DES(k, m)

    Args:
        m should be a bytestring (i.e. a sequence of characters such as 'Hello'
          or '\x02\x04')
        k should be a bytestring of length exactly 8 bytes.

    Note that for DES the key is given as 8 bytes, where the last bit of
    each byte is just a parity bit, giving the actual key of 56 bits, as
    expected for DES. The parity bits are ignored.

    Return:
        The bytestring ciphertext c
    """
    d = DES.new(k, DES.MODE_ECB)
    c = d.encrypt(m)
    return c


def des_dec(k, c):
    """
    Decrypt a message c with a key k using DES as follows:
    m = DES(k, c)

    Args:
        c should be a bytestring (i.e. a sequence of characters such as 'Hello'
          or '\x02\x04')
        k should be a bytestring of length exactly 8 bytes.

    Note that for DES the key is given as 8 bytes, where the last bit of
    each byte is just a parity bit, giving the actual key of 56 bits, as
    expected for DES. The parity bits are ignored.

    Return:
        The bytestring plaintext m
    """
    d = DES.new(k, DES.MODE_ECB)
    m = d.decrypt(c)
    return m


def des2_enc(k1, k2, m):
    # TODO 3.B: implement des2_enc
    return des_enc(k1, des_enc(k2, m))


def des2_dec(k1, k2, c):
    # TODO 3.B: implement des2_dec
    return des_dec(k2, des_dec(k1, c))


def main():
    k1 = 'Smerenie'
    k2 = 'Dragoste'
    m1_given = 'Fericiti cei saraci cu duhul, ca'
    c1 = 'cda98e4b247612e5b088a803b4277710f106beccf3d020ffcc577ddd889e2f32'
    c2 = '54826ea0937a2c34d47f4595f3844445520c0995331e5d492f55abcf9d8dfadf'

    # TODO 3.C: Decrypt c1 and c2 using k1 and k2, and make sure that 
    #           des2_dec(k1, k2, c1 || c2) == m1 || m2
    #
    # Note: The code to decrypt c1 is already provided below. You **need**
    # to decrypt c2 as well.
    #
    m1 = bytes_to_string(des2_dec(string_to_bytes(k1), string_to_bytes(k2),
                         bytes.fromhex(c1)))
    assert m1 == m1_given, f'Expected "{m1_given}", but got "{m1}"'

    print('ciphertext:', c1)
    print('plaintext:', m1)
    print('plaintext in hexa:', str_2_hex(m1))

    m2 = bytes_to_string(des2_dec(string_to_bytes(k1), string_to_bytes(k2),
                         bytes.fromhex(c2)))
    print('plaintext 2:', m2)
    print(bytes_to_string(des2_dec(string_to_bytes(k1), string_to_bytes(k2), bytes.fromhex(c1 + c2))), '==', m1 + m2)

    # TODO 3.D: run meet-in-the-middle attack for the following plaintext/ciphertext
    m1 = 'Pocainta'
    c1 = '9f98dbd6fe5f785d'
    m2 = 'Iertarea'
    c2 = '6e266642ef3069c2'

    # NOTE: you only need to search for the first 2 bytes of the each key (i.e.,
    # to find out what are the values for each `?`)
    k1_suffix = 'oIkvH5'
    k2_suffix = 'GK4EoU'

    t1 = []
    t2 = []
    for byte1 in range(0, 128):
        for byte2 in range(0, 128):
            first_2_bytes = chr(byte1) + chr(byte2)
            k1 = string_to_bytes(first_2_bytes + k1_suffix)
            k2 = string_to_bytes(first_2_bytes + k2_suffix)
            t1.append((k2, des_enc(k2, string_to_bytes(m1))))
            t2.append((k1, des_dec(k1, bytes.fromhex(c1))))
    
    t2s = sorted(t2, key=itemgetter(1))
    tenc = [value for _,value in t2s]
    keys = []
    for pair in t1:
        (k2, enc_msg) = pair
        index = get_index(tenc, enc_msg)
        if index == -1:
            continue

        (k1, _) = t2s[index]
        keys.append((k1, k2))

    for pair in keys:
        (k1, k2) = pair
        if des_enc(k2, string_to_bytes(m2)) == des_dec(k1, bytes.fromhex(c2)):
            print(k1, k2)

if __name__ == '__main__':
    main()