from caesar import *


def decrypt(ciphertext):
    plaintext = ''
    # TODO decrypt the ciphertext
    for i in range(1, 26):
        common_string = caesar_enc_string('YOU', i)
        if ciphertext.count(common_string) > 0:
            return caesar_dec_string(ciphertext, i)
    return plaintext


def main():
    ciphertexts = []
    with open("msg_ex1.txt", 'r') as f:
        for line in f:
            ciphertexts.append(line[:-1])
    print(ciphertexts)
    for c in ciphertexts:
        print(decrypt(c))


if __name__ == "__main__":
    main()
