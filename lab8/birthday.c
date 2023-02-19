#include <openssl/sha.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>

/* We want a collision in the first 4 bytes = 2^16 attempts */
#define N_BITS  16
#define MSG_NUM_BYTES 8

int raw2int4(unsigned char * digest) {
    int i;
    int sum = 0;

    for (i = 0; i < 3; i++) {
        sum += sum * 256 + digest[i];
    }

    return sum;
}

void hexdump(unsigned char * string, int length) {
    int i;
    for (i = 0; i < length; i++) {
        printf("%02x", string[i]);
    }
}

int run_attack(uint32_t attempt) {
/* Step 1. Generate 2^16 different random messages */
    int number_of_messages = pow(2, 16);
    char **messages = malloc(sizeof(char*) * number_of_messages);
    for (int i = 0; i < number_of_messages; i++) {
        messages[i] = malloc(sizeof(char) * MSG_NUM_BYTES);
        for (int j = 0; j < MSG_NUM_BYTES; j++) {
            messages[i][j] = (char) rand() % 256;
        }
    }   

    /* Step 2. Compute hashes */
    unsigned char **mds = malloc(sizeof(char*) * number_of_messages);
    for (int i = 0; i < number_of_messages; i++) {
        mds[i] = malloc(sizeof(unsigned char) * 20);
        SHA_CTX context;
        SHA1_Init(&context);
        SHA1_Update(&context, messages[i], MSG_NUM_BYTES);
        SHA1_Final(mds[i], &context);
    }

    /* Step 3. Check if there exist two hashes that match in the first four bytes */
    for (int i = 0; i < number_of_messages; i++) {
        for (int j = i + 1; j < number_of_messages; j++) {
            int are_equal = 1;
            for (int z = 0; z < 4; z++) {
                if (mds[i][z] != mds[j][z]) {
                    are_equal = 0;
                }
            }

            /* Step 3a. If a match is found, print the messages and hashes */
            if (are_equal) {
                printf("Found match... message1 - %s message2 - %s hash1 - %s hash2 - %s in %d attemps.\n", messages[i], messages[j], mds[i], mds[j], attempt);
                return 1;
            }
        }
    }

    return 0;
}

int main(int argc, char * argv[]) {
    uint32_t attempt = 1;     /* Iterate through 16 bits of the 32; use the rest to run different attacks */

    /* Try to find a collision on the first 4 bytes (32 bits) */
    srand(42);

    /* Step 3b. If no match is found, repeat the attack with a new set of random messages */
    int was_match_found = run_attack(attempt);
    while (!was_match_found) {
        attempt++;
        was_match_found = run_attack(attempt);
    }

    return 0;
}
