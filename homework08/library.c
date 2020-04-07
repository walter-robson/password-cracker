/* library.c: string utilities library */

#include "str.h"

#include <ctype.h>
#include <string.h>

/**
 * Convert all characters in string to lowercase.
 * @param   s       String to convert
 **/
void	str_lower(char *s) {
  for (char *c = s; *c; c++){
    *c = tolower( *c);
  }
  return;
}

/**
 * Convert all characters in string to uppercase.
 * @param   s       String to convert
 **/
void	str_upper(char *s) {
  for(char *c = s; *c; c++){
    *c = toupper( *c);
  }
  return;
}

/**
 * Convert all characters in string to titlecase.
 * @param   s       String to convert
 **/
void	str_title(char *s) {

  for(char*c = s; *c; c++){
      *s = toupper(*s); //makes the first character capitalized
      *c = tolower(*c); //makes the rest of characters lowercase
  }
  for(char*c = s; *c; c++){
    if(!isalpha(*c)){
      *(c+1) = toupper(*(c+1));
    }
  }
  return;
}

/**
 * Removes trailing newline (if present).
 * @param   s       String to modify
 **/
void    str_chomp(char *s) {
  if(*(s + strlen(s) - 1) == '\n'){
    *(s + strlen(s) - 1) = '\0';
  }
  return;
}

/**
 * Removes whitespace from front and back of string (if present).
 * @param   s       String to modify
 **/
void    str_strip(char *s) {
  char * pointer1 = s;
  char * pointer2 = s;
  if(*pointer1 == ' '){ //checks to make sure that the next steps are neccicary
    while(*pointer1 == ' '){
      pointer1++;
    }
    while(*pointer1 != '\0'){
      *pointer2 = *pointer1;
      *pointer1 = ' ';
      pointer1++;
      pointer2++;
    }
  }
  while(*(s+strlen(s) - 1) == ' '){
    *(s + strlen(s) - 1) = '\0';
  }
}

/**
 * Reverses a string.
 * @param   s       String to reverse
 **/
void    str_reverse(char *s) {
  char * head = s;
  char * tail = s + strlen(s) -1;
  while(head < tail){
    char temp;
    temp = *head;
    *head = *tail;
    *tail = temp;
    head++;
    tail--;
  }
}

/**
 * Replaces all instances of 'from' in 's' with corresponding values in 'to'.
 * @param   s       String to translate
 * @param   from    String with letter to replace
 * @param   to      String with corresponding replacment values
 **/
void    str_translate(char *s, char *from, char *to) {
  char lookup_table[1<<8] = {0};
  while(*from != '\0'){
    lookup_table[(int)*from]= *to;
    from++;
    to++;
  }

  while(*s != '\0'){
    if(lookup_table[(int)*s]){
      *s = lookup_table[(int)*s];
    }
    s++;
  }
}

/**
 * Converts given string into an integer.
 * @param   s       String to convert
 * @param   base    Integer base
 * @return          Converted integer value
 **/
int	str_to_int(const char *s, int base) {
    char * tail = s + strlen(s) -1;
    int sum;
    int count;
    int mult;
    if(!isalpha(*tail)){
      count = 0;
      sum = 0;
      mult = 1;
      while(tail > s){
        int num = *tail - 48;
        for(int i = 0; i<=count; i++)
          mult *= base;
        sum+= (num * mult);
        count++;
        tail--;
      }
    }

    return sum;
}

/* vim: set sts=4 sw=4 ts=8 expandtab ft=c: */
