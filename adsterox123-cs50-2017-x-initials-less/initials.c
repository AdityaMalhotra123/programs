//initials.c

//prints initials of the name inputed by user

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    //get user input
    string name = get_string();
    //safety check
    if (name != NULL)
    {
        //print first letter of name in uppercase
        printf("%c", toupper(name[0]));
        //iterate over each character in name
        for(int n = 0; n < strlen(name); n++)
        {
            //print first letter after each space
            if (name[n] == ' ')
            {
                printf("%c", toupper(name[n + 1]));
            }
        }
    }
    //newline to make output more neat and presentable
    printf("\n");
}