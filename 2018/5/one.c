#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>

int strip_letter(char *string, char letter)
{
    int match = 0;
    size_t in = 0, out = 0;

    while (isprint(string[in]))
    {
        if (toupper(string[in]) == toupper(letter))
        {
            match++;
        }
        else
        {
            string[out++] = string[in];
        }
        in++;
    }
    string[out] = '\0';
    return match;
}

int strip_dups(char *string)
{
    size_t in = 0, out = 0;
    int match = 0;
    char last = '\0';

    while (isprint(string[in]))
    {
        if ((toupper(last) == toupper(string[in])) &&
            (last != string[in]))
        {
            match++;
            if (out > 0) {
                out--; /* backup one space on output */
                string[out] = '\0';  /* clarifies printout */
            } else
                printf("Error: found dup when out = %ld\n", out);
            last = '\0'; /* prevent a immediate 3-char match: (cCc) */
        }
        else
        {
            last = string[in];
            string[out++] = string[in];
        }
        in++;
    }
    string[out] = '\0';
    return match;
}

int main (int argc, char *argv[])
{
    FILE *in;
    int i;
    size_t size;
    char *string;
    char *tmpstring;
    char letter;
    int results['Z'] = {0};
    char best_letter = 'A';

    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s datafile\n", argv[0]);
        return 1;
    }

    in = fopen(argv[1], "r");
    if (!in)
    {
        fprintf(stderr, "Could not open %s: %s\n", argv[1], strerror(errno));
        return 1;
    }

    fseek(in, 0L, SEEK_END);
    size = ftell(in) + 1;
    string = malloc(sizeof(char) * size);
    if (!string)
    {
        fprintf(stderr, "Could not malloc 1st %ld byte string.\n", size * sizeof(char));
        return 1;
    }
    fprintf(stderr, "Created 1st %ld byte string.\n", size * sizeof(char));
    tmpstring = malloc(sizeof(char) * size);
    if (!tmpstring)
    {
        fprintf(stderr, "Could not malloc 2nd %ld byte string.\n", size * sizeof(char));
        return 1;
    }
    fprintf(stderr, "Created 2nd %ld byte string.\n", size * sizeof(char));

    rewind(in);
    fread (string, 1, size - 1, in);

    printf("Striping");
    memcpy(tmpstring, string, size);
    while (strip_dups(tmpstring))
        printf(".");
    printf("\nAfter: %s\n", tmpstring);
    printf("Answer #1: %ld\n", strlen(tmpstring));

   
    for(letter = 'A'; letter <= 'Z'; letter++)
    {
        memcpy(tmpstring, string, size);
        strip_letter(tmpstring, letter);
//        printf("Strip '%c' yields: %s\n", letter, tmpstring);
        while (strip_dups(tmpstring))
        {
//        printf("\nAfter: %s\n", tmpstring);
        }
        printf("Answer #2-%c: %ld\n", letter, strlen(tmpstring));
        results[letter] = (int)strlen(tmpstring);
    }

    
    for(letter = 'A'; letter <= 'Z'; letter++)
    {
        if (results[letter] < results[best_letter])
        {
            best_letter = letter;
        }
    }
    printf("Answer #2: stripping '%c' yeilds %d\n", best_letter, results[best_letter]);

    printf("Cleanup!\n");
    free(tmpstring);
    free(string);
    fclose(in);
}
