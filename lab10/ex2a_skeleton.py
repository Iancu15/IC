import random
import math


def int2bin(val):
    """
    Convert a 4-bit value to binary and return it as a list.

    :param val: 4-bit positive value.

    :return l: list of the bits obtained when converting value to binary.
    """
    l = [0] * (4)

    l[0] = val & 0x1
    l[1] = (val & 0x2) >> 1
    l[2] = (val & 0x4) >> 2
    l[3] = (val & 0x8) >> 3

    return l


def generate(q=97, s=19, nr_values=20):
    """
    Generate the public key vectors A and B.

    :param q: Modulus
    :param s: Secret key
    :param nr_values: Length of vector variables

    :return A, B: Public key vectors, each with "nr_values" elements

        TODO 1: Generate public key A
           A = [a0, a1, ..., an-1] vector with random values. Of course values modulo q. :)

        TODO 2: Generate error vector e
           e = [e0, e1, ..., en-1] error vector with small errors in interval [1, 4]

        TODO 3: Compute public key B
           B = [b0, b1, ..., bn-1] with bi = ai * s + ei. Modulo q do not forget..

        TODO 4: Return public keys A, B
    """

    # TODO 1: Generate public key "A"
    #A = ...
    A = [random.uniform(0, 10000) % q for _ in range(nr_values)]

    # TODO 2: Generate error vector "e"
    #e = ...
    e = [random.uniform(1, 4) for _ in range(nr_values)]

    # TODO 3: Compute public key "B"
    #B = ...
    B = [(A[i] * s + e[i]) % q for i in range(nr_values)]

    # TODO 4: Return public keys A, B
    return A, B


def encrypt_bit(A, B, plain_bit, q=97):
    """
    Encrypt one bit using Learning with Errors(LWE).

    :param A: Public key
    :param B: Public key
    :param plain_bit: Plain bit that you want to encrypt
    :param q: Modulus

    :return: Cipher pair u, v

        TODO 1: Generate a list of 5 random indexes with which you will sample values from public keys A and B.
            random_sample_index_list = [random_index_1, random_index_2, ..., random_index_5]
            A sample for A is A[random_index_i] or for B is B[random_index_i].

        TODO 2: Compute "u"
            u = sum of the samples from vector A
            Don't forget modulo.

        TODO 3: Compute "v"
            v = sum of the samples from vector B + floor(q/2) * plain_bit
            Don't forget modulo.

        TODO 4: Return cipher pair u, v
    """

    # The pair (u, v) will be basically the cipher.
    u = 0
    v = 0

    # TODO 1: Generate a list of 5 random indexes with which you will sample values from both public keys A and B.
    random_sample_index_list = [random.randint(0, 19) for _ in range(5)]

    # TODO 2: Compute u
    #u = ...
    u = sum([A[i] for i in random_sample_index_list])

    # TODO 3: Compute v
    #v = ...
    v = sum([B[i] for i in random_sample_index_list])
    v += math.floor(q / 2) * plain_bit

    # TODO Return the cipher pair (u, v) reduced modulo q
    return (u % q, v % q)



def encrypt(A, B, number, q=97):
    """
    Encrypt a 4-bit number

    :param A: Public Key.
    :param B: Public Key.
    :param number: Number in interval [0, 15] that you want to encrypt.
    :param q: Modulus

    :return list with the cipher pairs (ui, vi).
    """
    # Convert number to binary; you will obtain a list with 4 bits
    bit_list = int2bin(number)

    # Using the function that you made before, encrypt each bit.
    u0, v0 = encrypt_bit(A, B, bit_list[0], q)
    u1, v1 = encrypt_bit(A, B, bit_list[1], q)
    u2, v2 = encrypt_bit(A, B, bit_list[2], q)
    u3, v3 = encrypt_bit(A, B, bit_list[3], q)

    return [(u0, v0), (u1, v1), (u2, v2), (u3, v3)]


def decrypt_bit(cipher_pair, s=19, q=97):
    """
    Decrypt a bit using Learning with errors.

    :param cipher_pair: Cipher pair (u, v)
    :param s: Secret key
    :param q: Modulus

        TODO 1: Compute the "dec" value with which you will decrypt the bit.
            dec = (v - s * u) modulo q

        TODO 2: Obtain and return the decrypted bit.
            The decrypted bit is 1 if the previously computed "dec" value is bigger than floor(q/2) and 0 otherwise.

    :return list with the cipher pairs (ui, vi).
    """

    # Extract pair (u, v) from the argument "cipher_pair".
    u = cipher_pair[0]
    v = cipher_pair[1]

    # TODO 1: Compute "dec" variable
    dec = (v - s * u) % q

    # TODO 2: Decrypt bit and return it
    if dec > math.floor(q / 2):
        return 1
    
    return 0

def decrypt(cipher, s=19, q=97):
    """
    Decrypt a 4-bit number from the cipher text pairs (ui, vi).

    :param cipher: Cipher text. List with 4 cipher pairs (u, v) corresponding to each encrypted bit
    :param s: Secret key
    :param q: Modulus

    :return plain: List with the 4 decrypted bits.
    """
    u1, v1 = cipher[0][0], cipher[0][1]
    u2, v2 = cipher[1][0], cipher[1][1]
    u3, v3 = cipher[2][0], cipher[2][1]
    u4, v4 = cipher[3][0], cipher[3][1]

    bit0 = decrypt_bit([u1, v1], s, q)
    bit1 = decrypt_bit([u2, v2], s, q)
    bit2 = decrypt_bit([u3, v3], s, q)
    bit3 = decrypt_bit([u4, v4], s, q)

    return [bit3, bit2, bit1, bit0]


if __name__ == "__main__":
    # Initialize Parameters
    q = 97
    s = 19
    nr_values = 20
    print("Initial parameters are:\n modulus={}\n secret_key={}\n nr_of_values={}\n".format(q, s, nr_values))

    # Integer in [0, 15] that you want to encrypt
    number_to_encrypt = 10
    print("You want to encrypt number " + str(number_to_encrypt))

    # Generate Step
    A, B = generate(q, s, nr_values)
    print("\nPublic Keys obtained:")
    print("A=", end="")
    print(A)
    print("B=", end="")
    print(B)

    # Encrypt Step
    cipher = encrypt(A, B, number_to_encrypt, q)
    print("\nCipher is ", end="")
    print(cipher)

    # Decrypt Step
    plain = decrypt(cipher, s, q)
    print("\nPlain value in binary is ", end="")
    print(plain)

    # If plain is the representation in binary of "number_to_encrypt" it should be fine but you can check with other numbers. :D