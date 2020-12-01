#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//#define VERBOSE 1

void inc(int *val, int amount, int max)
{
    *val += amount;
    if (*val >= max)
    {
        *val = *val - max;
    }
    else if (*val < 0)
    {
        *val = *val + max;
    }
}

int delete(int *data, int data_size, int place)
{
    int i;

    for(i = 0; i < place; i++)
    {
    }
    while( i++ < data_size)
    {
        data[i-1] = data[i];
    }
    return (i-2);
}

int insert_after(int *data, int data_size, int place, int val)
{
    int i;
    int backup, tmp;

    for(i = 0; i <= place; i++)
    {
    }
    backup = data[i];
    data[i] = val;
    while( i++ < data_size)
    {
        tmp = backup;
        backup = data[i];
        data[i] = tmp;
    }
    return (i);
}

int main (int argc, char *argv[])
{
    int i, top_player=0, players, marbles_in_play, max_marbles;
    int player=0, marble=0, cur = 0;
    int *data, *scores;

    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s players marbles\n", argv[0]);
        return 1;
    }
    
    players = atoi(argv[1]);
    max_marbles = atoi(argv[2]);

    data = malloc(sizeof(int) * max_marbles);
    if (!data)
    {
        fprintf(stderr, "Could not malloc game board (%ld bytes) \n", max_marbles * sizeof(int));
        return 1;
    }

    scores = malloc(sizeof(int) * (players+1));
    if (!scores)
    {
        fprintf(stderr, "Could not malloc high score data (%ld bytes) \n", (players+1) * sizeof(int));
        return 1;
    }
    memset(scores, 0, sizeof(int) * (players+1));

    printf("Players: %d\nMarbles: %d\n", players, max_marbles);

    data[0] = 0;  /* Setup board with 1 marble @ 0 */
    marbles_in_play = 1;  /* # of marbles in play */
    cur = 0;      /* current marble pointer (0 based) */
    player = 1;   /* start with player 1 */
    marble = 1;   

    while (marble <= max_marbles)
    {
#ifndef VERBOSE
        if ((marble % 1000) == 0)
        {
            printf("Player-%03d Marble-%08d\n", player, marble);
        }
#endif

        if ((marble % 23) == 0)
        {
            inc(&cur, -7, marbles_in_play);
            scores[player] = scores[player] + marble + data[cur];
#ifdef VERBOSE
            printf("Player %d: Marble #%d: special case: remove %d  score: %d  total_score: %d\n",  player, marble, data[cur], marble + data[cur], scores[player]);
//            printf("Player %d: delete a '%d' from position %d\n", player, data[cur], cur);
#endif
            marbles_in_play = delete(data, marbles_in_play, cur);
        }
        else
        {
            inc(&cur, 1, marbles_in_play);
#ifdef VERBOSE
//            printf("Player %d: insert a '%d' after position %d\n", player, marble, cur);
#endif
            marbles_in_play = insert_after(data, marbles_in_play, cur, marble);
            inc(&cur, 1, marbles_in_play);
        }

#ifdef VERBOSE
        printf("Player %d: [", player);
        for (i=0; i<marbles_in_play; i++)
        {
            if (i == marbles_in_play -1)
                printf("%d", data[i]);
            else
                printf("%d, ", data[i]);
        }
        printf("]\n");
#endif

        if (++player > players)
            player = 1;
        marble++;
    }

    for (i=1; i <= players; i++)
    {
        if (scores[i] > scores[top_player])
            top_player = i;
    }
    printf("Top score: Player-%d: %d\n", top_player, scores[top_player]);
}
