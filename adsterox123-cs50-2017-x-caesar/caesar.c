//caesar.c

//takes user input and encrypts it using a caesar cypher

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    //program works only if there are two arguments
    if (argc == 2)
    {
        //declare variables
        string key = argv[1];
        int k = atoi(key);
        char ciphertext;
        //get user input
        printf("plaintext: ");
        string plaintext = get_string();
        int i;
        printf("ciphertext: ");
        //encrypt - iterate over each caracter in the string (plaintext)
        for (i = 0; i < strlen(plaintext); i++)
        {
            //uppercase letters
            if (isupper(plaintext[i]))
            {
                //shift plaintext by key
                 ciphertext = ((plaintext[i] - 65) + k) % 26;
                 //print encrypted message character by character
                 printf("%c", ciphertext + 65);
            }
            //lowercase letters
            else if (islower(plaintext[i]))
            {
                //shift plaintext by key
                ciphertext = ((plaintext[i] - 97) + k) % 26;
                //print encrypted message character by character
                printf("%c", ciphertext + 97);
            }
            //if non-alphabet
            else
            {
                //print without shifting/changing 
                printf("%c", plaintext[i]);
            }
            
        }
        //newline to make the output more neat and presentable
        printf("\n");
        return 0;
    }
    //if there are more or less than two cammand line arguments
    else
    {
        //error message
        printf("Usage: ./caesar k\n");
        return 1;
    }
}