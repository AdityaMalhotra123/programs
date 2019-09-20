#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdint.h>
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover file_to_recover\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[1];

    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    int filecount = 0;
    BYTE buffer[512];
    FILE* temp = NULL;
    bool found = false;
    while (fread(buffer, 1, 512, inptr) != 0x00)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (!found)
            {
                found = true;
                char filename[8];
                sprintf(filename, "%03i.jpg", filecount);
                temp = fopen(filename, "w");
                filecount++;
                fwrite(buffer, 1, 512, temp);

            }
            else
            {
                fclose(temp);
                char filename[8];
                sprintf(filename, "%03i.jpg", filecount);
                temp = fopen(filename, "w");
                filecount++;
                fwrite(buffer, 1, 512, temp);
            }



        }
        else
        {
            if (found)
            {
                fwrite(buffer, 1 ,512, temp);
            }
        }
    }
    fclose(temp);
    fclose(inptr);

    return 0;
}



