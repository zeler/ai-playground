# Deep blue (research review)

The goal of this document is to summarize advancements in the field
of Artificial Intelligence (AI) while building chess machine able to 
defeat human chess grandmasters. Document is split in  multiple topics
as they were described by the reasearch paper.
 
## Hardware
Deep Blue is parallel system with focus on searching through chess
game trees. It is composed from 30 processor units and 480 single-chip 
chess search engines, which were able to quickly search through game 
tree.

System is built in three layers - one master processor which works 
as a supervisor while the rest function as slave nodes. Each slave node has 
control over multiple search engine chips. Thanks to this design, game tree (or at least its parts) could be searched in parallel, resulting in great increase in performance. Search (as well as initial search) is conducted by master node, which is delegating work among slave nodes.

The result of this design is high performance search and possibility
to implement hybrid software/hardware search. Thanks to this, developers
were able to have quick search using optimized hardware-based evaluation
function and use much more complex, software-based evaluation function
when needed.
 
## Evaluation function
Deep Blue team implemented complex software evaluation function with over 8000
different features. Most of them were implemented and tuned by hand
and automatic analysis tools were used to fine-tune evaluation function 
performance - one was used for detecting noisy features or features clusters
and second was used to tune evaluation function weights. 
 
## Opening book
Deep Blue uses opening book created by multiple chess grandmasters. Alongside
this, Deep Blue has also access to Extended book, which is a large database
of past games. An ad hoc search function was implemented and used to search
through this database. The weights were set in a way, which allowed Deep Blue 
to play moves without conducting search, if board state was found in the database.

## Endgame database
Large endgame database was also used for moves with 5 pieces or less. This 
could help to make more informed decisions but haven't proved to be critical
in practice. Interesting design decisions had to be made because of size of the database. Database was split into two parts - each chess chip stored its
own copy of important moves and everything else has been stored to external
storage.

## Time limits
Deep Blue did the search only in predefined time-frames. There were two time targets set before each search. First one was used in standard states and the second was used when the didn't work out well. There was also "time buffer" for handling technical difficulties and possible "sudden death" phase.  
 
# Summary
The goal of Deep Blue was to win match against World Chess Champion Garry 
Kasparov in 1997 and it was ultimately achieved as a result of multiple iterations of hardware and software development cycles. The
large searching capability, non-uniform search, and complex evaluation function were all critical. However, Deep Blue creators admit a lot of
improvements could be made to further improve the performance. Amongst
them, parallel search efficiency and hardware improvements were mentioned.
From software perspective, algorithm optimalizations (search tree pruning) 
and fine-tuned evaluation function could also help in terms of overall performance.