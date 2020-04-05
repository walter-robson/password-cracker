/* sum.c */

#include <stdio.h>
#include <stdlib.h>

/* Constants */

#define MAX_NUMBERS (1<<10)

/* Functions */

size_t read_numbers(FILE *stream, int numbers[], size_t n) {
    size_t i = 0;

    while (i < n && scanf("%d", &numbers[i]) != EOF){
        i++;
    }

    return i;
}

int compare(const void * a, const void * b)
{
  return(*(int*)a - *(int*)b);
}
/* Main Execution */

int main(int argc, char *argv[]) {
    int numbers[MAX_NUMBERS];
    size_t nsize;

    nsize = read_numbers(stdin, numbers, MAX_NUMBERS);
    qsort(numbers,nsize,sizeof(int),compare);

    for(int i = 0; i < nsize; i++){
      printf("%d\n",numbers[i]);
    }


    return EXIT_SUCCESS;
}
