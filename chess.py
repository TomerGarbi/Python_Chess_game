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
        self.white_king = (7, 4)
        self.black_king = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.moves_functions = {"P": self.get_pawn_moves, "R": self.get_rook_moves, "B": self.get_bishop_moves,
                                "N": self.get_knight_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}
        self.en_passant_square = ()
        self.castling_rights = CastlingRights(True, True, True, True)
        self.castling_rights_log = [CastlingRights(self.castling_rights.white_king_side, self.castling_rights.white_queen_side,
                                    self.castling_rights.black_king_side, self.castling_rights.black_queen_side)]

    def turn_color(self):
        if self.white_to_move:
            return "w"
        else:
            return "b"

    def update_castling_rights(self, move):
        if move.piece_moved == "wK":
            self.castling_rights.white_queen_side = False
            self.castling_rights.white_king_side = False
        elif move.piece_moved == "bK":
            self.castling_rights.black_queen_side = False
            self.castling_rights.black_king_side = False
        elif move.piece_moved == "wR":
            if move.start_row == 7:
                if move.start_col == 0:
                    self.castling_rights.white_queen_side = False
                elif move.start_col == 7:
                    self.castling_rights.white_king_side = False
        elif move.piece_moved == "bR":
            if move.start_row == 0:
                if move.start_col == 0:
                    self.castling_rights.black_queen_side = False
                elif move.start_col == 7:
                    self.castling_rights.black_king_side = False

    def make_move(self,  move):
        self.board[move.start_row][move.start_col] = "--"
        if move.is_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + move.promotion_choice
        else:
            self.board[move.end_row][move.end_col] = move.piece_moved
            if move.is_en_passant:
                self.board[move.start_row][move.end_col] = "--"
            elif move.castle:
                if move.end_col > move.start_col:
                    self.board[move.start_row][move.end_col - 1] = self.board[move.start_row][move.end_col + 1]
                    self.board[move.start_row][move.end_col + 1] = "--"
                else:
                    self.board[move.start_row][move.end_col + 1] = self.board[move.start_row][move.end_col - 2]
                    self.board[move.start_row][move.end_col - 2] = "--"
        self.move_log.append(move)
        if move.piece_moved[1] == 'K':
            if self.white_to_move:
                self.white_king = (move.end_row, move.end_col)
            else:
                self.black_king = (move.end_row, move.end_col)
        if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
            self.en_passant_square = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.en_passant_square = ()
        self.update_castling_rights(move)
        self.castling_rights_log.append(CastlingRights(self.castling_rights.white_king_side, self.castling_rights.white_queen_side,
                                    self.castling_rights.black_king_side, self.castling_rights.black_queen_side))
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if len(self.move_log) == 0:
            print("starting position")
        else:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            if move.piece_moved[1] == "K":
                if move.piece_moved[0] == "w":
                    self.white_king = (move.start_row, move.start_col)
                else:
                    self.black_king = (move.start_row, move.start_col)
            if move.is_en_passant:
                self.en_passant_square = (move.end_row, move.end_col)
                self.board[move.end_row][move.end_col] = "--"
            if move.castle:
                if move.end_col > move.start_col:
                    self.board[move.start_row][move.end_col + 1] = self.board[move.start_row][move.end_col - 1]
                    self.board[move.start_row][move.end_col - 1] = "--"
                else:
                    self.board[move.start_row][move.end_col - 2] = self.board[move.start_row][move.end_col + 1]
                    self.board[move.start_row][move.end_col + 1] = "--"

                self.board[move.start_row][move.end_col] = move.piece_captured
            if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
                self.en_passant_square = ()

            self.castling_rights_log.pop()
            self.castling_rights = self.castling_rights_log[-1]
            self.white_to_move = not self.white_to_move

    def get_pawn_moves(self, r, c, color, moves):
        if color == "w":    # white to move
            if r == 1:  # check for promotion
                if self.board[r-1][c] == "--":
                    for P in ["Q, R, B, N"]:
                        moves.append(Move((r, c), (r - 1, c), self.board, promotion_choice=P))
                if c < 7 and self.board[r - 1][c + 1][0] == "b":
                    for P in ["Q, R, B, N"]:
                        moves.append(Move((r, c), (r - 1, c + 1), self.board, promotion_choice=P))
                if c > 0 and self.board[r - 1][c - 1][0] == "b":
                    for P in ["Q, R, B, N"]:
                        moves.append(Move((r, c), (r - 1, c - 1), self.board, promotion_choice=P))
            else:
                if self.board[r - 1][c] == "--":
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r, c), (r - 2, c), self.board))
                if c < 7:
                    if self.board[r - 1][c + 1][0] == "b":
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
                    elif (r - 1, c + 1) == self.en_passant_square:
                        moves.append(Move((r, c), (r - 1, c + 1), self.board, en_passant=True))
                if c > 0:
                    if self.board[r - 1][c - 1][0] == "b":
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
                    elif (r - 1, c - 1) == self.en_passant_square:
                        moves.append(Move((r, c), (r - 1, c - 1), self.board, en_passant=True))

        else:   # black to move
            if r == 6:  # check for promotion
                if self.board[r + 1][c] == "--":
                    for P in ["Q, R, B, N"]:
                        moves.append(Move((r, c), (r + 1, c), self.board, promotion_choice=P))
                if c < 7 and self.board[r + 1][c + 1][0] == "w":
                    for P in ["Q, R, B, N"]:
                        moves.append(Move((r, c), (r + 1, c + 1), self.board, promotion_choice=P))
                if c > 0 and self.board[r + 1][c - 1][0] == "w":
                    for P in ["Q, R, B, N"]:
                        moves.append(Move((r, c), (r + 1, c - 1), self.board, promotion_choice=P))
            else:
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move((r, c), (r + 2, c), self.board))
                if c < 7:
                    if self.board[r + 1][c + 1][0] == "w":
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
                    elif (r + 1, c + 1) == self.en_passant_square:
                        moves.append(Move((r, c), (r + 1, c + 1), self.board, en_passant=True))
                if c > 0:
                    if self.board[r + 1][c - 1][0] == "w":
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                    elif (r + 1, c - 1) == self.en_passant_square:
                        moves.append(Move((r, c), (r + 1, c - 1), self.board, en_passant=True))

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
        if c < 6:   # right moves
            if r < 7 and self.board[r + 1][c + 2][0] != color:
                moves.append(Move((r, c), (r + 1, c + 2), self.board))
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
        while not stop and row <= 7 and col <= 7:   # down right moves
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
        while not stop and row <= 7 and col >= 0:  # down left moves
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
        while not stop and col >= 0:
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



    def get_castle_moves(self, r, c, color, moves):
        if self.square_under_attack(r, c):
            return
        elif color == "w":
            if self.castling_rights.white_king_side:
                if self.board[r][c + 1] == "--" and not self.square_under_attack(r, c + 1):
                    if self.board[r][c + 2] == "--" and not self.square_under_attack(r, c + 2):
                        moves.append(Move((r, c), (r, c + 2), self.board, castle=True))
            if self.castling_rights.white_queen_side:
                if self.board[r][c - 1] == "--" and not self.square_under_attack(r, c - 1):
                    if self.board[r][c - 2] == "--" and not self.square_under_attack(r, c - 2):
                        if self.board[r][c - 3] == "--":
                            moves.append(Move((r, c), (r, c - 2), self.board, castle=True))



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

    def square_under_attack(self, r, c):
        self.white_to_move = not self.white_to_move
        opponent_moves = self.get_all_possible_moves()
        for move in opponent_moves:
            if move.end_row == r and move.end_col == c:
                self.white_to_move = not self.white_to_move
                return True
        self.white_to_move = not self.white_to_move
        return False

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king[0], self.white_king[1])
        else:
            return self.square_under_attack(self.black_king[0], self.black_king[1])

    def get_valid_moves(self):
        temp_en_passant = self.en_passant_square
        possible_moves = self.get_all_possible_moves()
        temp_castling_rights = CastlingRights(self.castling_rights.white_king_side, self.castling_rights.white_queen_side,
                                              self.castling_rights.black_king_side, self.castling_rights.black_queen_side)
        for i in range(len(possible_moves) - 1, -1, -1):
            move = possible_moves[i]
            self.make_move(move)
            self.white_to_move = not self.white_to_move
            if self.in_check():
                possible_moves.remove(move)
            self.undo_move()
            self.white_to_move = not self.white_to_move
        if len(possible_moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        if self.white_to_move:
            self.get_castle_moves(self.white_king[0], self.white_king[1], "w", possible_moves)
        else:
            self.get_castle_moves(self.black_king[0], self.black_king[1], "b", possible_moves)
        self.en_passant_square = temp_en_passant
        self.castling_rights = temp_castling_rights
        return possible_moves


class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board, user_move=False, promotion_choice="", en_passant=False, castle=False):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_promotion = False
        self.promotion_choice = promotion_choice
        self.user_move = user_move
        self.castle = castle
        self.is_promotion = (self.piece_moved == "wP" and self.end_row == 0) or (self.piece_moved == "bP" and self.end_row == 7)
        self.is_en_passant = False
        self.is_en_passant = self.piece_moved[1] == "P" and en_passant
        if self.is_en_passant:
            self.piece_captured = "wP" if self.piece_moved == "bP" else "bP"

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


class CastlingRights:
    def __init__(self, white_king_side, white_queen_side, black_king_side, black_queen_side):
        self.white_king_side = white_king_side
        self.white_queen_side = white_queen_side
        self.black_king_side = black_king_side
        self.black_queen_side = black_queen_side

    def __str__(self):
        return f"{self.white_king_side} {self.white_queen_side} | {self.black_king_side} {self.black_queen_side}"


