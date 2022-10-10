class GameState:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}
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
        self.current_castling_rights = CastlingRights(True, True, True, True)
        self.castling_rights_log = [self.hard_copy_castling_rights(self.current_castling_rights)]
        self.pawn_or_captures = 0
        self.pawn_or_captures_log = [0]

    def turn_color(self):
        if self.white_to_move:
            return "w"
        else:
            return "b"

    def switch_turns(self):
        self.white_to_move = not self.white_to_move

    def hard_copy_castling_rights(self, castling_rights):
        return CastlingRights(castling_rights.white_king_side, castling_rights.white_queen_side,
                              castling_rights.black_king_side, castling_rights.black_queen_side)

    def update_castling_rights(self, move):
        if move.piece_moved == "wK":
            self.current_castling_rights.white_queen_side = False
            self.current_castling_rights.white_king_side = False
        elif move.piece_moved == "bK":
            self.current_castling_rights.black_king_side = False
            self.current_castling_rights.black_queen_side = False
        elif move.piece_moved == "wR":
            if move.start_row == 7:
                if move.start_col == 0:
                    self.current_castling_rights.white_queen_side = False
                elif move.start_col == 7:
                    self.current_castling_rights.white_king_side = False
        elif move.piece_moved == "bR":
            if move.start_row == 0:
                if move.start_col == 0:
                    self.current_castling_rights.black_queen_side = False
                elif move.start_col == 7:
                    self.current_castling_rights.black_king_side = False

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        if move.is_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + move.promotion_choice
        else:
            self.board[move.end_row][move.end_col] = move.piece_moved
            if move.is_en_passant:
                self.board[move.start_row][move.end_col] = "--"
            if move.castle_move:
                if move.start_col < move.end_col:   # king side castling
                    self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = "--"
                else:
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                    self.board[move.end_row][move.end_col - 2] = "--"
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
        self.castling_rights_log.append(self.hard_copy_castling_rights(self.current_castling_rights))
        self.pawn_or_captures_log.append(self.pawn_or_captures)
        if move.piece_moved == "P" or move.is_capture:
            self.pawn_or_captures = 0
        else:
            self.pawn_or_captures += 1
        self.switch_turns()


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
                self.board[move.start_row][move.end_col] = move.piece_captured
            if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
                self.en_passant_square = ()
            if move.castle_move:
                if move.start_col <= move.end_col:
                    self.board[move.end_row][move.end_col + 1] = move.piece_captured
                    self.board[move.end_row][move.end_col - 1] = "--"
                    self.board[move.end_row][move.end_col] = "--"
                else:
                    self.board[move.end_row][move.end_col - 2] = move.piece_captured
                    self.board[move.end_row][move.end_col + 1] = "--"
                    self.board[move.end_row][move.end_col] = "--"
            self.castling_rights_log.pop()
            self.current_castling_rights = self.hard_copy_castling_rights(self.castling_rights_log[-1])
            self.pawn_or_captures = self.pawn_or_captures_log.pop()
            self.switch_turns()

    def get_pawn_moves(self, r, c, color, moves):
        promotion_options = ["Q", "R", "B", "N"]
        if color == "w":    # white to move
            if r == 1:  # check for promotion
                if self.board[r-1][c] == "--":
                    for P in promotion_options:
                        moves.append(Move((r, c), (r - 1, c), self.board, promotion_choice=P))
                if c < 7 and self.board[r - 1][c + 1][0] == "b":
                    for P in promotion_options:
                        moves.append(Move((r, c), (r - 1, c + 1), self.board, promotion_choice=P))
                if c > 0 and self.board[r - 1][c - 1][0] == "b":
                    for P in promotion_options:
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
                    for P in promotion_options:
                        moves.append(Move((r, c), (r + 1, c), self.board, promotion_choice=P))
                if c < 7 and self.board[r + 1][c + 1][0] == "w":
                    for P in promotion_options:
                        moves.append(Move((r, c), (r + 1, c + 1), self.board, promotion_choice=P))
                if c > 0 and self.board[r + 1][c - 1][0] == "w":
                    for P in promotion_options:
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
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for d in directions:
            row, col = r + d[0], c + d[1]
            stop = False
            while not stop and 0 <= row <= 7 and 0 <= col <= 7:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    row += d[0]
                    col += d[1]
                elif self.board[row][col][0] != color:
                    moves.append(Move((r, c), (row, col), self.board))
                    stop = True
                else:
                    stop = True

    def get_rook_moves(self, r, c, color, moves):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for d in directions:
            row, col = r + d[0], c + d[1]
            stop = False
            while not stop and 0 <= row <= 7 and 0 <= col <= 7:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    row += d[0]
                    col += d[1]
                elif self.board[row][col][0] != color:
                    moves.append(Move((r, c), (row, col), self.board))
                    stop = True
                else:
                    stop = True

    def get_queen_moves(self, r, c, color, moves):
        self.get_rook_moves(r, c, color, moves)
        self.get_bishop_moves(r, c, color, moves)

    def get_king_moves(self, r, c, color, moves):
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

    def get_king_side_castling(self, r, c, color, moves):
        if not self.in_check():
            if self.board[r][c + 1] == "--" and not self.square_under_attack(r, c + 1):
                if self.board[r][c + 2] == "--" and not self.square_under_attack(r, c + 2):
                    moves.append(Move((r, c), (r, c + 2), self.board, castle_move=True))

    def get_queen_side_castling(self, r, c, color, moves):
        if not self.in_check():
            if self.board[r][c - 1] == "--" and not self.square_under_attack(r, c - 1):
                if self.board[r][c - 2] == "--" and not self.square_under_attack(r, c - 2):
                    if self.board[r][c - 3] == "--":
                        moves.append(Move((r, c), (r, c - 2), self.board, castle_move=True))

    def get_castling_moves(self, r, c, color, moves):
        if color == 'w':
            if self.current_castling_rights.white_king_side:
                self.get_king_side_castling(r, c, color, moves)
            if self.current_castling_rights.white_queen_side:
                self.get_queen_side_castling(r, c, color, moves)
        else:
            if self.current_castling_rights.black_king_side:
                self.get_king_side_castling(r, c, color, moves)
            if self.current_castling_rights.black_queen_side:
                self.get_queen_side_castling(r, c, color, moves)

    def get_all_possible_moves(self, include_castling=False):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece_type, piece_color = self.board[r][c][1], self.board[r][c][0]
                if(piece_color == "w" and self.white_to_move) or (piece_color == "b" and not self.white_to_move):
                    self.moves_functions[piece_type](r, c, piece_color, moves)
                    if include_castling and piece_type == "K":
                        self.get_castling_moves(r, c, piece_color, moves)
        return moves

    def square_under_attack(self, r, c):
        self.switch_turns()
        opponent_moves = self.get_all_possible_moves()
        for move in opponent_moves:
            if move.end_row == r and move.end_col == c:
                self.switch_turns()
                return True
        self.switch_turns()
        return False

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king[0], self.white_king[1])
        else:
            return self.square_under_attack(self.black_king[0], self.black_king[1])

    def get_valid_moves(self):
        temp_en_passant = self.en_passant_square
        possible_moves = self.get_all_possible_moves(include_castling=True)
        for i in range(len(possible_moves) - 1, -1, -1):
            move = possible_moves[i]
            self.make_move(move)
            self.switch_turns()
            if self.in_check():
                possible_moves.remove(move)
            self.undo_move()
            self.switch_turns()
        if len(possible_moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        self.en_passant_square = temp_en_passant
        return possible_moves


    def FEN(self):
        fen = ""
        for i in range(len(self.board)):
            empty_squares = 0
            for j in range(len(self.board[i])):
                piece = self.board[i][j]
                if piece == "--":
                    empty_squares += 1
                else:
                    if empty_squares != 0:
                        fen += str(empty_squares)
                        empty_squares = 0
                    if piece[0] == "w":
                        fen = fen + piece[1]
                    else:
                        fen = fen + piece[1].lower()
            if empty_squares != 0:
                fen = fen + str(empty_squares)
            if i != 7:
                fen = fen + "/"
        if self.white_to_move:
            fen += " w "
        else:
            fen += " b "
        fen += self.current_castling_rights.get_FEN()
        if self.en_passant_square != ():
            fen += " " + str(self.en_passant_square[0]) + self.cols_to_files(self.en_passant_square[1]) + " "
        else:
            fen += " - "
        fen += str(self.pawn_or_captures) + " " + str(len(self.move_log) // 2 + 1)
        return fen


class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board, user_move=False, promotion_choice="", en_passant=False, castle_move=False):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_promotion = False
        self.promotion_choice = promotion_choice
        self.user_move = user_move
        self.is_promotion = (self.piece_moved == "wP" and self.end_row == 0) or (self.piece_moved == "bP" and self.end_row == 7)
        self.is_en_passant = False
        self.is_en_passant = self.piece_moved[1] == "P" and en_passant
        self.castle_move = castle_move
        self.is_capture = self.piece_captured != "--"
        if self.castle_move:
            self.piece_captured = f"{self.piece_moved[0]}R"
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
        return f"white: {self.white_king_side}, {self.white_queen_side} | black: {self.black_king_side}, {self.black_queen_side}"

    def get_FEN(self):
        fen = ""
        if self.white_king_side:
            fen += "K"
        if self.white_queen_side:
            fen += "Q"
        if self.black_king_side:
            fen += "k"
        if self.black_queen_side:
            fen += "q"
        if fen != "":
            return fen
        else:
            return "-"