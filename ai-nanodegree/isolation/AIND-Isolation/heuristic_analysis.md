# Isolation game - AI heuristic analysis

This document compares three different heuristics in the Isolation game.
Comparison is made using pre-made python script

    tournament.py
    
which is bundled in the Isolation project sources. Comparison is made
against result of agent with 'improved score' heuristic 
used as a benchmark which takes computer performance into account.

## Heuristic 1 - Count number of blank spaces around legal moves
This heuristic takes into account number of blank spaces around each
possible legal move in given move. The idea behind this heuristic is 
that the more blank spaces are around legal moves the more moves will 
be possible to play in the future and vice versa for opponent, where 
we are trying to minimize number of blank moves around him. The priority
for minimizing blank spaces for opponent is slightly higher than maximizing
blank spaces for player.

# Heuristic 2 - Check for corners and walls
This heuristic is an improved version of 'Improved score' which takes
into account count of player and opponent legal moves. The improvement
is made by checking if landing moves are near walls and corners for the
opponent as this will further limit possibility for moves in the future.
The resulting effect of this heuristic is we are actively trying to chase
opponent into board corners.

# Heuristic 3 - Combined heuristic

This heuristic is the combination of the previous two and thus is 
the most complex. In early stages of the game, we use the second
heuristic as it's faster than the other one. In later stages of the 
game we try to count blank spaces around every move. Combination
of these two metrics yields better results overall.

# Results

As the best heuristic was selected heuristic AB_Custom - Combined heuristic which had better overall performance 
than  other heurisic functions.

| Match # |  Opponent | AB_Improved | AB_Custom |  AB_Custom_2 | AB_Custom_3|
|---------|-----------|-------------|-----------|--------------|------------|
|    1    |   Random  |     9  -  1 |    8  -  2 |    6  -  4|     7  -  3|
|    2    |   MM_Open  |    2  -  8 |    5  -  5 |    2  -  8|     5  -  5|
|    3    |  MM_Center  |   6  -  4 |    4  -  6 |    7  -  3|     6  -  4|
|    4    | MM_Improved |   3  -  7 |    3  -  7|     3  -  7|     5  -  5|
|    5    |   AB_Open   |   5  -  5 |    9  -  1 |   5  -  5|     6  -  4|
|    6    |  AB_Center  |   5  -  5 |    5  -  5 |    4  -  6|     7  -  3|
|    7    | AB_Improved |   5  -  5 |    5  -  5|     3  -  7|     6  -  4|
|         |  Win Rate:  |    50.0%   |     55.7%    |    42.9%   |    60.0%|