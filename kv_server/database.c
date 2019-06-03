#include <malloc.h>
#include <stdio.h>
#include <string.h>

struct entry {
    char* key;
    char* value;
};

static struct entry* database;
static size_t size = 0;

int db_extend(int new_size)
{
    int idx;

    if (new_size <= size) {
        return -1;
    }

    database = realloc(database, new_size * sizeof(struct entry));

    if (database == NULL) {
        return -1;
    };
    for (idx = size; idx < new_size - 1; idx++) {
        database[idx].key = NULL;
        database[idx].value = NULL;
    }

    size = new_size;
    return 0;
}

int db_insert(char* key, char* value)
{
    int idx;
    char* new_key;
    char* new_value;

    for (idx = 0; idx < size; idx++) {
        if (database[idx].key == NULL) {
            new_key = malloc(strlen(key) + 1);
            strcpy(new_key, key);

            new_value = malloc(strlen(value) + 1);
            strcpy(new_value, value);

            database[idx].key = new_key;
            database[idx].value = new_value;
            return idx;
        }
    }

    if (db_extend(size + 10) == -1) {
        return -1;
    }
    return db_insert(key, value);
}

int db_find(char* key)
{
    struct entry current;
    int idx;

    for (idx = 0; idx < size; idx++) {
        current = database[idx];
        if (current.key != NULL) {
            if (strcmp(key, current.key) == 0) {
                return idx;
            }
        }
    }
    return -1;
}

int db_update(int idx, char* value)
{
    char* new_value;
    new_value = malloc(strlen(value) + 1);
    strcpy(new_value, value);

    database[idx].value = new_value;
    return 0;
}

int db_put(char* key, char* value)
{
    int idx;

    idx = db_find(key);
    if (idx == -1) {
        return db_insert(key, value);
    } else {
        return db_update(idx, value);
    }
}

char* db_get(char* key)
{
    int idx;
    idx = db_find(key);
    if (idx == -1) {
        return NULL;
    } else {
        return database[idx].value;
    }
}

#ifndef DBLIB
int main(void)
{
    db_put("foo", "bar");
    printf("%s\n", db_get("foo"));

    db_put("foo", "baz");
    db_put("qqq", "baz");

    printf("%s\n", db_get("foo"));
    printf("%s\n", db_get("qqq"));

    return 0;
}
#endif