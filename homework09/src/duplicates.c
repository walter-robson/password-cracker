/* duplicates.c */

#include "hash.h"
#include "macros.h"
#include "table.h"

#include <dirent.h>
#include <limits.h>
#include <sys/stat.h>

/* Globals */

char * PROGRAM_NAME = NULL;

/* Structures */

typedef struct {
    bool count;
    bool quiet;
} Options;

/* Functions */

void usage(int status) {
    fprintf(stderr, "Usage: %s paths...\n", PROGRAM_NAME);
    fprintf(stderr, "    -c     Only display total number of duplicates\n");
    fprintf(stderr, "    -q     Do not write anything (exit with 0 if duplicate found)\n");
    exit(status);
}

/**
 * Check if path is a directory.
 * @param       path        Path to check.
 * @return      true if Path is a directory, otherwise false.
 */
bool is_directory(const char *path) {
    struct stat buffer;
    if(stat(path, &buffer) != 0){
      return false;
    }
    return S_ISDIR(buffer.st_mode);
}

/**
 * Check if file is in table of checksums.
 *
 *  If quiet is true, then exit if file is in checksums table.
 *
 *  If count is false, then print duplicate association if file is in
 *  checksums table.
 *
 * @param       path        Path to file to check.
 * @param       checksums   Table of checksums.
 * @param       options     Options.
 * @return      0 if Path is not in checksums, otherwise 1.
 */
size_t check_file(const char *path, Table *checksums, Options *options) {
    char hexdigest[HEX_DIGEST_LENGTH];
    char buffer[BUFSIZ];

    if(hash_from_file(path, hexdigest)){
      Value *exists = table_search(checksums, hexdigest);
      if(exists){
        if(options->quiet){
          table_delete(checksums);
          exit(0);
        }
        else if(!(options->count)){
          printf("%s is a duplicate of %s\n", exists->string, path);
          return 1;
        }
        else{
          return 1;
        }
      }
      else{
        sprintf(buffer, "%s\n", path);
        table_insert(checksums, hexdigest, (Value)buffer, STRING);
      }
    }
    return 0;
}

/**
 * Check all entries in directory (recursively).
 * @param       root        Path to directory to check.
 * @param       checksums   Table of checksums.
 * @param       options     Options.
 * @return      Number of duplicate entries in directory.
 */
size_t check_directory(const char *root, Table *checksums, Options *options) {
    int num = 0;
    char buffer[BUFSIZ];

    DIR *dp = opendir(root);

    if(!dp){
        return 0;
    };

    for (struct dirent *d = readdir(dp); d; d = readdir(dp)) {
      if((strcmp(d->d_name,".") == 0) || (strcmp(d->d_name, "..") == 0)){
        continue;
      }
      sprintf(buffer, "%s/%s", root, d->d_name);
      if(d->d_type == DT_DIR){
        num += check_directory(buffer, checksums, options);
      }
      else if(d->d_type == DT_REG){
        num +=  check_file(buffer, checksums, options);
      }
    }
    closedir(dp);
    return num;
}

/* Main Execution */

int main(int argc, char *argv[]) {
    /* Parse command line arguments */
    PROGRAM_NAME = argv[0];
    if(argc == 1){
      usage(0);
    }
    Options options = {false, false};
    int count = 0;

    Table *hashtable = table_create(0);

    for(int i = 1; i < argc; i++){
      if(argv[i][0] == '-'){
        if(argv[i][1] == 'h') usage(0);
        if(argv[i][1] == 'q') options.quiet = true;
        if(argv[i][1] == 'c') options.count = true;
      }
      /* Check each argument */
      else
      {
        if(is_directory(argv[i])){
          count += check_directory(argv[i], hashtable, &options);
        }
        else {
          count += check_file(argv[i], hashtable, &options);
        }
      }
    }

    /* Display count if necessary */
    if(options.count){
      printf( "%d\n", count);
    }
    if(options.quiet){
      table_delete(hashtable);
      return EXIT_FAILURE;
    }

    table_delete(hashtable);

    return EXIT_SUCCESS;
}

/* vim: set sts=4 sw=4 ts=8 expandtab ft=c: */
