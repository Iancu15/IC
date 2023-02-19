import math
from ex2a_skeleton import *

def xor_then_decrypt_bit(cipher_pair1, cipher_pair2, s=19, q=97):
    """
    Xor Cipher pairs and then decrypt a bit using Learning with errors.

    :param cipher_pair1: First cipher pair (u, v)
    :param cipher_pair2: Second cipher pair (u, v)
    :param s: Secret key
    :param q: Modulus

        TODO 1: Compute the "dec" value with which you will decrypt the bit.
            dec = ((v_1 - s * u_1) + (v_2 - s * u_2)) % q

        TODO 2: Obtain and return the decrypted bit.
            The decrypted bit is 1 if the previously computed "dec" value is bigger than floor(q/2) and 0 otherwise.

    :return the decrypted bit
    """

    # Extract pair (u, v) from the argument "cipher_pair".
    u_1 = cipher_pair1[0]
    v_1 = cipher_pair1[1]

    u_2 = cipher_pair2[0]
    v_2 = cipher_pair2[1]


    # TODO 1: Compute "dec" variable
    dec = ((v_1 - s * u_1) + (v_2 - s * u_2)) % q

    # TODO 2: Decrypt bit and return it
    if dec > math.floor(q / 2):
        return 1
    
    return 0


def xor_then_decrypt(cipher1, cipher2, s=19, q=97):
    """
    Bit wise xor the two cipher pairs and the decrypt 4-bit number result.

    :param cipher1: Cipher 1.
    :param cipher2: Cipher 2.
    :param s: Secret key
    :param q: Modulus

    :return plain: List with the 4 decrypted bits.
    """
    u1_1, v1_1 = cipher1[0][0], cipher1[0][1]
    u2_1, v2_1 = cipher1[1][0], cipher1[1][1]
    u3_1, v3_1 = cipher1[2][0], cipher1[2][1]
    u4_1, v4_1 = cipher1[3][0], cipher1[3][1]

    u1_2, v1_2 = cipher2[0][0], cipher2[0][1]
    u2_2, v2_2 = cipher2[1][0], cipher2[1][1]
    u3_2, v3_2 = cipher2[2][0], cipher2[2][1]
    u4_2, v4_2 = cipher2[3][0], cipher2[3][1]

    bit0 = xor_then_decrypt_bit([u1_1, v1_1], [u1_2, v1_2], s, q)
    bit1 = xor_then_decrypt_bit([u2_1, v2_1], [u2_2, v2_2], s, q)
    bit2 = xor_then_decrypt_bit([u3_1, v3_1], [u3_2, v3_2], s, q)
    bit3 = xor_then_decrypt_bit([u4_1, v4_1], [u4_2, v4_2], s, q)

    return [bit3, bit2, bit1, bit0]

if __name__ == "__main__":
    nr_values = 20
    number1 = 5
    number2 = 10
    A, B = generate(nr_values)
    cipher1 = encrypt(A, B, number1)
    cipher2 = encrypt(A, B, number2)
    print('XOR between plaintext:', number1 ^ number2)

    result = xor_then_decrypt(cipher1, cipher2)
    print('The decrypted XOR between cipher texts:', result)
    # 15 = [1, 1, 1, 1] in binar, metoda a functionat