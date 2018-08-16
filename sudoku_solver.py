#------------------------------------------------------------------------------
def solve(board):
    """
    Takes a 9x9 board and solves it

    Empty positions are represented by "."
    """

    # Init
    row_candidates = [set(str(x) for x in range(1, 10)) for _ in range(9)]
    col_candidates = [set(str(x) for x in range(1, 10)) for _ in range(9)]
    square_candidates = [
                            [set(str(x) for x in range(1, 10)) for _ in range(3)] 
                        for y in range(3)]

    empty_squares = set()

    # Parse board
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
    
    return board
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def _solve(empty_squares, board, row_candidates, 
                    col_candidates, square_candidates):
    """
    """
    if len(empty_squares) == 0:
        return True

    row, col, candidates = choose_square(empty_squares, row_candidates, 
                                        col_candidates, square_candidates)
    
    for candidate in candidates:
        make_move(board, row, col, empty_squares, candidate, 
                row_candidates, col_candidates, square_candidates)

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
    """
    candidates = row_candidates[row_no] & col_candidates[col_no] & \
                square_candidates[row_no // 3][col_no // 3]

    return candidates
#------------------------------------------------------------------------------
