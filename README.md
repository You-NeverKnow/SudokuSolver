# SudokuSolver
A very basic sudoku solver using backtracking.

## Algorithm:
1. Guess a solution for a blank square on the board.
	- Nine Persistent row, column, and big-square sets are maintained that keep track of all  
		the numbers that are not yet present in that rol, column, big-square respectively
	- Possible solutions for a square are obtained by set intersection of that 
		square's row, column, and big-square set.
	- Then, choose one of the possible numbers for that square.

2. Guess solutions for all squares. Backtrack if a square is still empty,
	but has no candidates for its solution.

3. A complete solution is found when all squares are filled.

## Proof of correctness:
Since for every square, we only chose a number that is consistent with its row, column, and big-square
Sudoku property is maintained. Thus, if all squares are filled, it implies that the puzzle is solved.

## Optimization:
### Choosing most constrained square for each step
Both, choosing an arbitrary square, or choosing the most constrained square, 
lead to a correct solution. However, choosing the most constrained square for next 
iteration works a lot faster. For easy puzzles(there is at least one square on 
board at all times with only one possible solution), we won't have to 
backtrack at all, reducing the complexity of the solver from 9^n to n^2. 

By choosing a square with fewer choices (say 3) as opposed to a square 
with 5 choices is an enormous win, since it multiplies for each position.
If we have 20 positions to fill, we must enumerate only 3^20 (about 3 million) solutions. 
A branching factor of 5 at each of the 20 positions will result in over
27000 times as much work!
