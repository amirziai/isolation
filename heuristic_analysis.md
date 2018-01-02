# Heuristic Analysis

### Heuristic 1
First heuristic was to use the difference of number of legal moves left between the player and the opponent. This heuristic works OK but was not beating `ID_Improved`. I tried making the agent more or less aggressive with changing the multiplier applied to both the player and opponent but did not find any consistent results. 

### Heuristic 2
Multiplied heuristic 1 by the reciprocal of the number of blank spaces left on the board. This scores the same position higher as the game progresses. 

### Heuristic 3
Uses a ratio of movements left times the number of squares left on the board so effectively taking into account both the relative opportunities and the stakes of the game. This is similar conceptually to the previous heuristic. A very helpful exercise was to try to vary a parameter added to both numerator and denominator that effectively controls how aggressive the player is. 

Heuristic | ID_Improve performance | Heuristic performance | Better
--- | --- | --- | ---
Heuristic 1 | 69.29% | 53.57% | 
Heuristic 2 | 70.00% | 64.29% | 
Heuristic 3 | 70.71% | 72.14% | &#10003;

### Recommendation
Heuristic 3 consistently outperforms ID_Improve. Since it takes into account both the progression of the game as well as the relative opportunity (moves left) and is tuned to right level of aggressiveness it's working well. Aggression in this context is the ability to take moves away from the opponent. So the less moves the opponent has the higher this score will be. This took a lot of experimentation which helped me build some intuition about the game that in turn led me to the right set of parameters. The search for the right evaluation function (other than the parameters) cannot be automated and found using an optimization algorithm and seems like knowing a lot about the problem is highly relevant for this piece.
