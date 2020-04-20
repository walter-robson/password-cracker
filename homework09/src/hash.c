/* hash.c: hash functions */

#include "hash.h"
#include <openssl/md5.h>
#include <stdio.h>
#include <unistd.h>

/**
 * Constants
 * http://isthe.com/chongo/tech/comp/fnv/
 */

#define FNV_OFFSET_BASIS    (0xcbf29ce484222325ULL)
#define FNV_PRIME           (0x100000001b3ULL)

/**
 * Compute FNV-1 hash.
 * @param   data            Data to hash.
 * @param   n               Number of bytes in data.
 * @return  Computed hash as 64-bit unsigned integer.
 */
uint64_t    hash_from_data(const void *data, size_t n) {
    uint64_t hash = FNV_OFFSET_BASIS;
    uint8_t *bytes = (uint8_t *) data; //thanks for the lecture example Bui!
    for(int i = 0; i < n; i++){
      hash = hash ^ bytes[i];
      hash = hash * FNV_PRIME;
    }
    return hash;
}

/**
 * Compute MD5 digest.
 * @param   path            Path to file to checksum.
 * @param   hexdigest       Where to store the computed checksum in hexadecimal.
 * @return  Whether or not the computation was successful.
 */
bool        hash_from_file(const char *path, char hexdigest[HEX_DIGEST_LENGTH]) {
    MD5_CTX context;
    uint8_t rawdigest[MD5_DIGEST_LENGTH];
    char buff[BUFSIZ];
    size_t bytes;

    MD5_Init(&context);
    FILE *sourcefile = fopen(path, "r");
    if(!sourcefile){
      return false;
    }

    bytes = fread(buff, 1, BUFSIZ, sourcefile );

    while (bytes > 0){
      MD5_Update(&context, buff, bytes);
      bytes = fread(buff, 1, BUFSIZ, sourcefile );
    }


    MD5_Final(rawdigest, &context);

    for (int i = 0; i < MD5_DIGEST_LENGTH; i++){
      sprintf(hexdigest + 2*i, "%02x", rawdigest[i]);
    }

    return true;
}

/* vim: set sts=4 sw=4 ts=8 expandtab ft=c: */
