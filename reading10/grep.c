#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Globals */

char * PROGRAM_NAME = NULL;

/* Functions */

void usage(int status) {
    fprintf(stderr, "Usage: %s\n", PROGRAM_NAME);
    exit(status);
}


/* Main Execution */

int main(int argc, char *argv[]) {
    int argind = 1;

    /* Parse command line arguments */
    PROGRAM_NAME = argv[0];
    while (argind < argc && strlen(argv[argind]) > 1 && argv[argind][0] == '-'){
        char *arg = argv[argind++];
        switch (arg[1]) {
            case 'h':
                usage(0);
                break;
            default:
                usage(1);
                break;
        }
    }

    string ret = strstr(argv[2],argv[1]);

    return 0;
}

/* vim: set sts=4 sw=4 ts=8 expandtab ft=c: */
