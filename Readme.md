This codebase has just been migrated out of the YACAI repo untested.

Resources used to design the code this far:
 - https://www.chessprogramming.org/Retrograde_Analysis
 - https://www.chessprogramming.org/Endgame_Tablebases
 - (And also more, I didn't bookmark all the sources unfortunately - ask me if you need something)

TODO (in no particular order):
 - Make the unmove generator work with pawns on the board 
 - Make the unmove generator more time efficient (potentially using my fast C++ chess engine, but not till much later probably)
 - Completely rework composition representation
 - Implement a general indexing function that works for all compositions (or several that each work on a subset if a truly general one is too challenging)
 - Implement all the optimizations in the paper at :
	https://www.researchgate.net/publication/44897543_Space-efficient_Indexing_of_Chess_Endgame_Tables
 - Implement Hoffman compression
 - Write a verification program to verify a tablebase