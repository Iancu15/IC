#include <openssl/evp.h>
#include <openssl/err.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

void hexdump(unsigned char * string, int length) {
    int i;
    for (i = 0; i < length; i++) {
        printf("%02x", string[i]);
    }
}


int aes_gcm_encrypt(unsigned char * ptext,
        int plen,
        unsigned char * key,
        unsigned char * iv,
        unsigned char ** ctext,
        int * clen) {

    EVP_CIPHER_CTX * ctx;
    int tmp_len;

    /* TODO Create new EVP Context */
    ctx = EVP_CIPHER_CTX_new();
    EVP_CIPHER_CTX_init(ctx);

    /* TODO Initialize context using 256-bit AES-GCM, Encryption operation */
    /* TODO Initialize Key and IV for the new context */
    EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, key, iv);

    /* TODO Encrypt data */
    if(!EVP_EncryptUpdate(ctx, *(ctext), clen, ptext, plen)) {
        /* Error */
        EVP_CIPHER_CTX_cleanup(ctx);
        return 0;
    }

    /* TODO Finalize encryption context (computes and appends auth tag) */
    if(!EVP_EncryptFinal_ex(ctx, *(ctext) + *clen, &tmp_len)) {
        /* Error */
        EVP_CIPHER_CTX_cleanup(ctx);
        return 0;
    }

    /* TODO Print tag */
    printf("%s\n", *(ctext) + *clen);
    *clen += tmp_len;

    /* TODO Destroy context */
    EVP_CIPHER_CTX_cleanup(ctx);

    return 0;
}

int aes_gcm_decrypt(unsigned char * ctext,
        int clen,
        unsigned char * key,
        unsigned char * iv,
        unsigned char ** ptext,
        int * plen) {

    EVP_CIPHER_CTX * ctx;
    int tmp_len;

    /* TODO Create new EVP Context */
    ctx = EVP_CIPHER_CTX_new();
    EVP_CIPHER_CTX_init(ctx);

    /* TODO Initialize context using 256-bit AES-GCM, Decryption operation */
    /* TODO Initialize Key and IV for the new context */
    EVP_DecryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, key, iv);

    /* TODO Submit tag data */
    /* TODO Decrypt data */
    if(!EVP_DecryptUpdate(ctx, *(ptext), plen, ctext, clen)) {
        /* Error */
        EVP_CIPHER_CTX_cleanup(ctx);
        return 0;
    }

    /* TODO Finalize decryption context (verifies auth tag) */
    if(!EVP_DecryptFinal_ex(ctx, *(ptext) + *plen, &tmp_len)) {
        /* Error */
        EVP_CIPHER_CTX_cleanup(ctx);
        return 0;
    }

    /* TODO Destroy context */
    EVP_CIPHER_CTX_cleanup(ctx);

    return 0;
}

int main(int argc, char * argv[]) {
    ERR_load_crypto_strings();

    unsigned char key[] = "0123456789abcdef0123456789abcdef"; /* 256-bit key */
    unsigned char iv[] = "0123456789ab";                      /* 96-bit IV   */

    unsigned char * ptext = (unsigned char *)"Hello, SSLWorld!\n";
    int plen = strlen((const char *)ptext);

    unsigned char * ctext;
    ctext = malloc(sizeof(unsigned char) * 100);
    int clen;

    printf("Plaintext = %s\n", ptext);
    printf("Plaintext  (hex) = "); hexdump(ptext, plen); printf("\n");

    aes_gcm_encrypt(ptext, plen, key, iv, &ctext, &clen);
    printf("Ciphertext (hex) = "); hexdump(ctext, clen - 16); printf("\n");

    unsigned char * ptext2;
    ptext2 = malloc(sizeof(unsigned char) * 100);
    int plen2;
    aes_gcm_decrypt(ctext, clen, key, iv, &ptext2, &plen2);
    printf("Done decrypting!\n");

    ptext2[plen2] = '\0';
    printf("Plaintext = %s\n", ptext2);

    if (memcmp(ptext, ptext2, strlen((const char *)ptext)) == 0) {
        printf("Ok!\n");
    } else {
        printf("Not ok :(\n");
    }

    return 0;
}
