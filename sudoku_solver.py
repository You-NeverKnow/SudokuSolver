#------------------------------------------------------------------------------
def main(stringified_board):
    """
    1. Parses stringified board into a 2D list
    2. Validates the sudoku board
    3. Solves the puzzle
    4. Returns the output in flat line string
    """
    
    # Parse board
    board = unstringify_board(stringified_board)
    
    # Validate sudoku puzzle
    if not is_valid_sudoku(board):
        return "Invalid sudoku puzzle"
    
    # Solve sudoku
    solve(board)
    
    # Stringify output board
    return "".join([x for row in range(9) for x in board[row]])
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def unstringify_board(stringified_board):
    """
    Converts string form of board to 2d list
    """
    board = [[] for x in range(9)]

    for i in range(9):
        row_start = 9*i
        board[i] = list(stringified_board[row_start: row_start + 9])
    
    return board
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def is_valid_sudoku(board):
    """
    Checks if an input sudoku board is valid

    Algorithm:
    For all non-empty squares on board, if value at that square is a number,
    check if the that value exists in that square's row, column, 
    and minor square.

    If it is, return False.
    """
    
    cols = [set() for _ in range(9)]
    squares = [[set() for _ in range(3)] for x in range(3)]
    
    for row in range(9):
        rows = set()
        for col in range(9):
            if board[row][col] == ".":
                continue
            # Check row
            if board[row][col] in rows:
                return False
            else:
                rows.add(board[row][col])

            # Check col
            if board[row][col] in cols[col]:
                return False
            else:
                cols[col].add(board[row][col])

            # Check square 
            if board[row][col] in squares[row // 3][col // 3]:
                return False
            else:
                squares[row // 3][col // 3].add(board[row][col])
    
    return True
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def solve(board):
    """
    Takes a 9x9 board and solves it
    Empty positions are represented by "."

    Initilizes variables required to solve sudoku puzzle, and solves it.
    """

    # Init: Set()s that keep track of numbers encountered in each row, col 
    # and big square
    row_candidates = [set(str(x) for x in range(1, 10)) for _ in range(9)]
    col_candidates = [set(str(x) for x in range(1, 10)) for _ in range(9)]
    square_candidates = [
                        [set(str(x) for x in range(1, 10)) for _ in range(3)] 
                        for y in range(3)]

    # Keeps track of squares that still are not filled
    empty_squares = set()

    # Parse board state
    for row in range(9):
        for col in range(9):
            if board[row][col].isdigit():
                update_sets(board[row][col], row, col, 
                            row_candidates, col_candidates, square_candidates)
            else:
                empty_squares.add((row, col))
    
    # Solve
    _solve(empty_squares, board, row_candidates, 
                    col_candidates, square_candidates)
    
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def _solve(empty_squares, board, row_candidates, 
                    col_candidates, square_candidates):
    """
    Algorithm:
    1. Choose the square that is most constrained: one that has least options.
    2. For all its candidate solutions, recursively repeat step 1 for next step.

    """

    # Exit condition: All squares filled
    if len(empty_squares) == 0:
        return True

    # Select next square
    row, col, candidates = choose_square(empty_squares, row_candidates, 
                                        col_candidates, square_candidates)
    
    # For all possible solutions for a square, find solutions for other squares
    for candidate in candidates:
        make_move(board, row, col, empty_squares, candidate, 
                row_candidates, col_candidates, square_candidates)

        # If a globaal solution is found, return all the way back
        if _solve(empty_squares, board, row_candidates, 
                col_candidates, square_candidates):
            return True
        
        unmake_move(board, row, col, empty_squares, candidate, 
                row_candidates, col_candidates, square_candidates)    
    
    return False
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def choose_square(empty_squares, 
                            row_candidates, col_candidates, square_candidates):
    """
    Iterates through all the squares, and returns the most constrained squares.
    
    Constrained factor is defined as length of intersection of that 
    square's row, column and encompassing square's sets
    """
    current_square_choice = None
    current_candidates = None
    min_candidates = float("inf")

    for row, col in empty_squares:
        candidates = get_candidates(row, col, row_candidates, 
                                    col_candidates, square_candidates) 
        if len(candidates) == 0:
            return row, col, candidates

        if len(candidates) < min_candidates:
            current_square_choice = (row, col)
            min_candidates = len(candidates)
            current_candidates = candidates
    
    return current_square_choice[0], current_square_choice[1], current_candidates   
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def make_move(board, row, col, empty_squares, candidate, 
                row_candidates, col_candidates, square_candidates):
    """
    Change all variables associated with making a move in the puzzle
    """
    update_sets(candidate, row, col, 
                row_candidates, col_candidates, square_candidates)
    empty_squares.discard((row, col))
    board[row][col] = candidate

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def unmake_move(board, row, col, empty_squares, candidate, 
                row_candidates, col_candidates, square_candidates):
    """
    Change back all variables changed while making a move in the puzzle
    """
    unupdate_sets(candidate, row, col,
                 row_candidates, col_candidates, square_candidates)
    empty_squares.add((row, col))
    board[row][col] = "."

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def unupdate_sets(ch, row, col, 
                    row_candidates, col_candidates, square_candidates):
    """
    """
    row_candidates[row].add(ch)
    col_candidates[col].add(ch)
    square_candidates[row // 3][col // 3].add(ch)

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def update_sets(ch, row, col, 
                        row_candidates, col_candidates, square_candidates):
    """
    """
    row_candidates[row].discard(ch)
    col_candidates[col].discard(ch)
    square_candidates[row // 3][col // 3].discard(ch)

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def get_candidates(row_no, col_no, 
                        row_candidates, col_candidates, square_candidates):
    """
    Gets possible candidates for a square with 3-way set intersection of its
    row, col and encompassing square sets
    """
    candidates = row_candidates[row_no] & col_candidates[col_no] & \
                square_candidates[row_no // 3][col_no // 3]

    return candidates
#------------------------------------------------------------------------------
