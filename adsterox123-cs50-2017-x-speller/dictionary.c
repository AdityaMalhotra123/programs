/**
 * Implements a dictionary's functionality.
 */
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


#include "dictionary.h"
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;
#define HASHTABLE_SIZE 65536
int words = 0;
bool loaded;
node* hashtable[HASHTABLE_SIZE];
int hash_function(const char *word)
{
    int hash = (tolower(word[0]) - 'a') % 26;
    return hash;
}
/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    int len = strlen(word);
    char word_copy[len + 1];

    // convert word to lowercase and store it in word_copy
    for (int i = 0; i < len; i++)
    {
       word_copy[i] = tolower(word[i]);
    }

    // add null terminator to end of char array
    word_copy[len] = '\0';

    // get hash value (a.k.a. bucket)
    int bucket = hash_function(word_copy);

    // assign cursor node to the first node of the bucket
    node *cursor = hashtable[bucket];

    // check until the end of the linked list
    while (cursor != NULL)
    {
        if (strcmp(cursor->word, word_copy) == 0)
        {
            // word is in dictionary
            return true;
        }
        else
        {
            // check next node
            cursor = cursor->next;
        }
    }
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }


    node *new_node;
    while (true)//while (fscanf(dict, "%s", word) != EOF)
    {
        /*new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }
        strcpy(new_node -> word, word);
        int index = hash_function(new_node -> word);*/
        new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }

        // read a word from the dictionary and store it in new_node->word
        fscanf(dict, "%s", new_node->word);
        new_node->next = NULL;

        if (feof(dict))
        {
            // hit end of file
            free(new_node);
            break;
        }

        words++;

        // hashtable[h] is a pointer to a key-value pair
        int h = hash_function(new_node->word);
        node* head = hashtable[h];

        // if bucket is empty, insert the first node
        if (head == NULL)
        {
            hashtable[h] = new_node;
        }
        // if bucket is not empty, attach node to front of list
        // design choice: unsorted linked list to minimize load time rather
        // than sorted linked list to minimize check time
        else
        {
            new_node->next = hashtable[h];
            hashtable[h] = new_node;
        }
    }
    loaded = true;
    fclose(dict);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    if (loaded)
    {
       return words;
    }
    else
    {
        return 0;
    }
}


/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    for (int i = 0; i < 65536; i++)
    {
        node *z = hashtable[i];
        while (z != NULL)
        {
            node *temp = z;
            z = z -> next;
            free(temp);
        }
    }
    loaded = false;
    return true;
}
