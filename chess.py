class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
                 ]
        self.white_to_move = True
        self.move_log = []
        self.moves_functions = {"P": self.get_pawn_moves, "R": self.get_rook_moves, "B": self.get_bishop_moves,
                                "N": self.get_knight_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}

    def make_move(self,  move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if len(self.move_log) == 0:
            print("starting position")
        else:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def get_pawn_moves(self, r, c, color, moves):   # TODO: add en passant and promotion
        if color == "w":    # white to move
            if r == 1:  # check for promotion
                pass
            else:
                if self.board[r - 1][c] == "--":
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r, c), (r - 2, c), self.board))
                if c < 7 and self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                if c > 0 and self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))

        else:   # black to move
            if r == 6:  # check for promotion
                pass
            else:
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move((r, c), (r + 2, c), self.board))
                if c < 7 and self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                if c > 0 and self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))

    def get_knight_moves(self, r, c, color, moves):
        if r > 1:   # up moves
            if c > 0 and self.board[r - 2][c - 1][0] != color:
                moves.append(Move((r, c), (r - 2, c - 1), self.board))
            if c < 7 and self.board[r - 2][c + 1][0] != color:
                moves.append(Move((r, c), (r - 2, c + 1), self.board))
        if r < 6:   # down moves
            if c > 0 and self.board[r + 2][c - 1][0] != color:
                moves.append(Move((r, c), (r + 2, c - 1), self.board))
            if c < 7 and self.board[r + 2][c + 1][0] != color:
                moves.append(Move((r, c), (r + 2, c + 1), self.board))
        if c > 1:   # left moves
            if r < 7 and self.board[r + 1][c - 2][0] != color:
                moves.append(Move((r, c), (r + 1, c - 2), self.board))
            if r > 0 and self.board[r - 1][c - 2][0] != color:
                moves.append(Move((r, c), (r - 1, c - 2), self.board))
        if c < 6:   # left moves
            if r < 7 and self.board[r + 1][c + 2][0] != color:
                moves.append(Move((r, c), (r - 1, c + 2), self.board))
            if r > 0 and self.board[r - 1][c + 2][0] != color:
                moves.append(Move((r, c), (r - 1, c + 2), self.board))

    def get_bishop_moves(self, r, c, color, moves):
        row, col = r - 1, c - 1
        stop = False
        while not stop and row >= 0 and col >= 0:   # up left moves
            if self.board[row][col] == "--":
                moves.append(Move((r, c), (row, col), self.board))
                row -= 1
                col -= 1
            elif self.board[row][col][0] != color:
                moves.append(Move((r, c), (row, col), self.board))
                stop = True
            else:
                stop = True
        row, col = r - 1, c + 1
        stop = False
        while not stop and row >= 0 and col <= 7:   # up right moves
            if self.board[row][col] == "--":
                moves.append(Move((r, c), (row, col), self.board))
                row -= 1
                col += 1
            elif self.board[row][col][0] != color:
                moves.append(Move((r, c), (row, col), self.board))
                stop = True
            else:
                stop = True
        row, col = r + 1, c + 1
        stop = False
        while not stop and row <= 7 and col <= 7:   # down left moves
            if self.board[row][col] == "--":
                moves.append(Move((r, c), (row, col), self.board))
                row += 1
                col += 1
            elif self.board[row][col][0] != color:
                moves.append(Move((r, c), (row, col), self.board))
                stop = True
            else:
                stop = True
        row, col = r + 1, c - 1
        stop = False
        while not stop and row <= 7 and col <= 7:  # down left moves
            if self.board[row][col] == "--":
                moves.append(Move((r, c), (row, col), self.board))
                row += 1
                col -= 1
            elif self.board[row][col][0] != color:
                moves.append(Move((r, c), (row, col), self.board))
                stop = True
            else:
                stop = True

    def get_rook_moves(self, r, c, color, moves):
        row, col = r - 1, c
        stop = False
        while not stop and row >= 0:  # up moves
            if self.board[row][col] == "--":
                moves.append(Move((r, c), (row, col), self.board))
                row -= 1
            elif self.board[row][col][0] != color:
                moves.append(Move((r, c),(row, col), self.board))
                stop = True
            else:
                stop = True
        row, col = r + 1, c     # down moves
        stop = False
        while not stop and row <= 7:
            if self.board[row][col] == "--":
                moves.append(Move((r, c), (row, col), self.board))
                row += 1
            elif self.board[row][col][0] != color:
                moves.append(Move((r, c), (row, col), self.board))
                stop = True
            else:
                stop = True
        row, col = r, c - 1
        stop = False
        while not stop and c >= 0:
            if self.board[row][col] == "--":
                moves.append(Move((r, c), (row, col), self.board))
                col -= 1
            elif self.board[row][col][0] != color:
                moves.append(Move((r, c), (row, col), self.board))
                stop = True
            else:
                stop = True
        row, col = r, c + 1
        stop = False
        while not stop and col <= 7:
            if self.board[row][col] == "--":
                moves.append(Move((r, c), (row, col), self.board))
                col += 1
            elif self.board[row][col][0] != color:
                moves.append(Move((r, c), (row, col), self.board))
                stop = True
            else:
                stop = True
    def get_queen_moves(self, r, c, color, moves):
        self.get_rook_moves(r, c, color, moves)
        self.get_bishop_moves(r, c, color, moves)

    def get_king_moves(self, r, c, color, moves):   # TODO: add castling
        if r > 0:   # up moves
            if c > 0 and self.board[r - 1][c - 1][0] != color:
                moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if self.board[r - 1][c][0] != color:
                moves.append(Move((r, c), (r - 1, c), self.board))
            if c < 7 and self.board[r - 1][c + 1][0] != color:
                moves.append(Move((r, c), (r - 1, c + 1), self.board))
        if r < 7:   # down moves
            if c > 0 and self.board[r + 1][c - 1][0] != color:
                moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if self.board[r + 1][c][0] != color:
                moves.append(Move((r, c), (r + 1, c), self.board))
            if c < 7 and self.board[r + 1][c + 1][0] != color:
                moves.append(Move((r, c), (r + 1, c + 1), self.board))
        if c > 0 and self.board[r][c - 1][0] != color:
            moves.append(Move((r, c), (r, c - 1), self.board))
        if c < 7 and self.board[r][c + 1][0] != color:
            moves.append(Move((r, c), (r, c + 1), self.board))

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece_type, piece_color = self.board[r][c][1], self.board[r][c][0]
                if(piece_color == "w" and self.white_to_move) or (piece_color == "b" and not self.white_to_move):
                    self.moves_functions[piece_type](r, c, piece_color, moves)
        return moves

    def get_king_position(self, color):
        for r in self.board:
            if f"{color}K" in r:
                return r, r.index(f"{color}K")
        return -1, -1

    def get_valid_moves(self):
        possible_moves = self.get_all_possible_moves()
        if self.white_to_move:
            king = self.get_king_position("w")
        else:
            king = self.get_king_position("b")
        for i in range(len(possible_moves) - 1, -1, -1,):
            move = possible_moves[i]
            self.make_move(move)
            opponent_moves = self.get_all_possible_moves()
            for m in opponent_moves:
                if m.end_row == king[0] and m.end_col == king[1]:
                    possible_moves.remove(move)
            self.undo_move()
        return possible_moves




class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    def get_file_rank(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def get_chess_notation(self):
        if self.piece_captured != "--":
            return self.get_file_rank(self.start_row, self.start_col) + "x" + self.get_file_rank(self.end_row, self.end_col)
        return self.get_file_rank(self.start_row, self.start_col) + self.get_file_rank(self.end_row, self.end_col)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.start_row == other.start_row and self.start_col == other.start_col\
                   and self.end_row == other.end_row and self.end_col == other.end_col
        return False





