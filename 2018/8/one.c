#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>

static int sum = 0;
static int new_node_name = 0;

/* Parse a node (recursively) */
int get_node(FILE *file, int name)
{
    int i, num_child, num_meta;
    int metadata[16];  /* should malloc, but I checked and max is 11 */
    int eachvalue[16] = {0};  /* should malloc, but I checked and max is 8 */
    int value = 0;

    /* Read the header */
    fscanf(file, "%d %d ", &num_child, &num_meta);
        
    /* Recurse! */
    for(i=0; i<num_child; i++)
    {
        eachvalue[i] = get_node(file, new_node_name++);
    }

    /* Print results */
    printf("Node-%04d:  Children: %d   Num_Meta: %d  Metadata: ", name, num_child, num_meta);
    for(i=0; i<num_meta; i++)
    {
        fscanf(file, "%d ", &metadata[i]);
        printf("%d ", metadata[i]);
        sum += metadata[i];  /* running sum for answer #1 */
        if (num_child == 0)
        {
            value += metadata[i];
        }
        else
        {
            /* metadata points to 1 based node numbers, but we store everything 0 based */
            value += eachvalue[metadata[i]-1];
        }
    }
    printf("  Value: %d\n", value);

    return value;
}

int main (int argc, char *argv[])
{
    FILE *in;
    int value;

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

    value = get_node(in, new_node_name++);
    printf("\nAnswer #1: Metadata Total: %d\n", sum);
    printf("Answer #2: Node-A Value: %d\n", value);

    fclose(in);
}
