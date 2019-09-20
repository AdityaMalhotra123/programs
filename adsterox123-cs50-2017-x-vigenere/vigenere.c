//vigenere.c

//Takes user input and encrypts it using a vigenere cypher

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>


int main(int argc, string argv[])
{
    //only accepts two cammand line arguments
    if (argc != 2)
    {
        //error message
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    //declare variables
    string key = argv[1];
    int ciphertext;
    int i;
    int j;
    int k;
    //iterate through the key to make sure it's alphabetical
    for (j = 0; j < strlen(key); j++)
    {
        if ((key[j] >= '0') && (key[j] <= '9'))
        {
            //error message
            printf("Usage: ./vigenere k\n");
            return 1;
        }
    }
    //get the plaintext
    printf("plaintext: ");
    string plaintext = get_string();
    printf("ciphertext: ");
    //encrypt - iterate over the characters in the string (plaintext)
    for (i = 0, j = 0; i < strlen(plaintext); i++, j++)
    {
        //go to the first letter of the key if the key is shorter than the plaintext
        if (j >= strlen(key))
        {
            j = 0;
        }
        //encrypt only alphabets, not non-alphabets
        if (isalpha(plaintext[i]))
        {
            //uppercase letters
            if (isupper(key[j]))
            {
                //get key value
                k = key[j] - 'A';
            }
            //lowercase letters
            else if (islower(key[j]))
            {
                //get key value
                k = key[j] - 'a';                
            }
            //uppercase letters
            if (isupper(plaintext[i]))
            {
                //shift plaintext by key value
                ciphertext = (((int)plaintext[i] - 65) + k) % 26;
                //print encrypted message character by character
                printf("%c", (char)ciphertext + 65);
            }
            //lowercase letters
            else if (islower(plaintext[i]))
            {
                //shift plaintext by key value
                ciphertext = (((int)plaintext[i] - 97) + k) % 26;
                //print encrypted message character by character
                printf("%c", (char)ciphertext + 97);
            }
        }
        //if non-alphabets
        else
        {
            //print without shifting/changing
            printf("%c", plaintext[i]);
            j = (j - 1);
        }
    }
    //newline to make the output more neat and presentable
    printf("\n");
    return 0;
}
