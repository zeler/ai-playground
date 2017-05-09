# Isolation game - AI heuristic analysis

This document compares three different heuristics in the Isolation game.
Comparison is made using pre-made python script

    tournament.py
    
which is bundled in the Isolation project sources. Comparison is made
against result of agent with 'improved score' heuristic 
used as a benchmark which takes computer performance into account.

As the best heuristic was selected heuristic number 3 - Combined heuristic.
   
## Heuristic 1 - Count number of blank spaces around legal moves
This heuristic takes into account number of blank spaces around each
possible legal move in given move. The idea behind this heuristic is 
that the more blank spaces are around legal moves the more moves will 
be possible to play in the future and vice versa for opponent, where 
we are trying to minimize number of blank moves around him. The priority
for minimizing blank spaces for opponent is slightly higher than maximizing
blank spaces for player.

|Opponent|ID_Improved|Student|
|--------|-----------|-------|
|Random|17 - 3|17 - 3|
|MM_Null|16 - 4|18  - 2|
|MM_Open|15 - 5|16 - 4|
|MM_Improved|13 - 7|12 - 8|
|AB_Null|16 - 4|15 - 5|
|AB_Open|14 - 6|13 - 7|
|AB_Improved|16 - 4|17 - 3|

Results:
----------
ID_Improved         76.43%
Student             77.14%

# Heuristic 2 - Check for corners and walls
This heuristic is an improved version of 'Improved score' which takes
into account count of player and opponent legal moves. The improvement
is made by checking if landing moves are near walls and corners for the
opponent as this will further limit possibility for moves in the future.
The resulting effect of this heuristic is we are actively trying to chase
opponent into board corners.

|Opponent|ID_Improved|Student|
|--------|-----------|-------|
|Random|18 - 2|17 - 3|
|MM_Null|12 - 8|16 - 4|
|MM_Open|14 - 6|16 - 4|
|MM_Improved|15 - 5|12 - 7|
|AB_Null|17 - 3|17 - 3|
|AB_Open|12 - 8|17 - 3|
|AB_Improved|18 - 2|14 - 6|

Results:
----------
ID_Improved         75.71%
Student             77.86%

# Heuristic 3 - Combined heuristic

This heuristic is the combination of the previous two and thus is 
the most complex. In early stages of the game, we use the second
heuristic as it's faster than the other one. In later stages of the 
game we try to count blank spaces around every move. Combination
of these two metrics yields better results overall.


|Opponent|ID_Improved|Student|
|--------|-----------|-------|
|Random|18 - 2|20 - 0|
|MM_Null|15 - 5|17 - 3|
|MM_Open|11 - 9|15 - 5|
|MM_Improved|14 - 6|15 - 5|
|AB_Null|17 - 3|15 - 5|
|AB_Open|20 - 0|16 - 4|
|AB_Improved|15 - 5|16 - 4|

Results:
----------
ID_Improved         78.57%
Student             81.43%
