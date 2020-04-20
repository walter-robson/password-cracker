/* table.c: Separate Chaining Hash Table */

#include "table.h"
#include "hash.h"
#include "macros.h"

/**
 * Create Table data structure.
 * @param   capacity        Number of buckets in the hash table.
 * @return  Allocated Table structure.
 */
Table *	    table_create(size_t capacity) {
    if(capacity == 0){
      capacity = DEFAULT_CAPACITY;
    }

    Table table[capacity];

    Table *t = calloc(1, sizeof(table));

    t->capacity = capacity;
    t->size = 0;
    t->buckets = calloc(capacity, sizeof(Pair));


    return t;
}

/**
 * Delete Table data structure.
 * @param   t               Table data structure.
 * @return  NULL.
 */
Table *	    table_delete(Table *t) {
    for(int i = 0; i < t->capacity; i++){
      if(t->buckets[i].next){
        pair_delete(t->buckets[i].next, true);
      }
    }
    free(t->buckets->value.string);
    free(t->buckets);

    free(t);

    return NULL;
}

/**
 * Insert or update Pair into Table data structure.
 * @param   m               Table data structure.
 * @param   key             Pair's key.
 * @param   value           Pair's value.
 * @param   type            Pair's value's type.
 */
void        table_insert(Table *t, const char *key, const Value value, Type type) {
    //I got help from Matt Tressler on this
    uint64_t bucket = hash_from_data(key, strlen(key)) % t->capacity;
    Pair *temppair = t->buckets[bucket].next;

    if(temppair){
      if(streq(temppair->key, key)){
        pair_update(temppair, value, type);
        return;
      }
      while(temppair->next){
        temppair = temppair->next;
        if(streq(temppair->key, key)){
          pair_update(temppair, value, type);
          return;
        }
      }
      temppair->next = pair_create(key, value, NULL, type);
      t->size += 1;
    }
    else{
      t->buckets[bucket].next = pair_create(key, value, NULL, type);
      t->size += 1;
    }
    return;

}

/**
 * Search Table data structure by key.
 * @param   t               Table data structure.
 * @param   key             Key of the Pair to search for.
 * @return  Pointer to the Value associated with specified key (or NULL if not found).
 */
Value *     table_search(Table *t, const char *key) {
  uint64_t bucket = hash_from_data(key, strlen(key)) % t->capacity;
  Pair *temppair = t->buckets[bucket].next;
  if(temppair){
    if(streq(temppair->key, key)){
      return &(temppair->value);
    }
    while(temppair->next){
      temppair = temppair->next;
      if(streq(temppair->key, key)){
        return &(temppair->value);
      }
    }
    return NULL;
  }
  else return NULL;

}

/**
 * Remove Pair from Table data structure with specified key.
 * @param   t               Table data structure.
 * @param   key             Key of the Pair to remove.
 * return   Whether or not the removal was successful.
 */
bool        table_remove(Table *t, const char *key) {
  uint64_t bucket = hash_from_data(key, strlen(key)) % t->capacity;
  Pair *curr = t->buckets[bucket].next;
  Pair *prev = &(t->buckets[bucket]);

  if(curr){
    if(streq(curr->key, key)){
      prev->next = curr->next;
      pair_delete(curr, false);
      t->size -= 1;
      return true;
    }
    while(curr->next){
      prev = curr;
      curr = curr->next;
      if(streq(curr->key, key)){
        prev->next = curr->next;
        pair_delete(curr, false);
        t->size -= 1;
        return true;
      }
    }
    return false;
  }
  else return false;

  return false;
}

/**
 * Format all the entries in the Table data structure.
 * @param   m               Table data structure.
 * @param   stream          File stream to write to.
 */
void	    table_format(Table *t, FILE *stream) {

  for(int i = 0; i < t->capacity; i ++ ){
    Pair *curr = t->buckets[i].next;
    if(curr){
      pair_format(curr, stream);
      while(curr->next){
        curr = curr->next;
        pair_format(curr, stream);
      }
    }
  }

}

/* vim: set sts=4 sw=4 ts=8 expandtab ft=c: */
