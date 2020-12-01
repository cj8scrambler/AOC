#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

//#define VERBOSE 1
#define NUMBER 1

int main (int argc, char *argv[])
{
    FILE *in;
    int *data;

    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s data\n", argv[0]);
        return 1;
    }
    
    in = fopen(argv[1],"r");
    if (!in)
    {
        fprintf(stderr, "Could not open %s: %s\n", argv[1], strerror(errno));
        return 1;
    }
    
    data = malloc(sizeof(int) * NUMBER);
    if (!data)
    {
        fprintf(stderr, "Could not malloc game board (%ld bytes) \n", NUMBER * sizeof(int));
        return 1;
    }
    memset(data, 0, sizeof(int) * (NUMBER));


    fclose(in);
}
