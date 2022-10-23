import chess
from stockfish import Stockfish


def engine_move_to_Move(engine_move):
    pass


engine = Stockfish(path="./stockfish_14.1_win_x64_avx2.exe")
gs = chess.GameState()
start_fen = gs.FEN()
fen = "8/7P/k7/8/8/8/K7/8 w - - 15 49"
engine.set_fen_position(fen)
engine_move = engine.get_best_move()
move = chess.Move((gs.ranks_to_rows[engine_move[1]], gs.files_to_cols[engine_move[0]]), (gs.ranks_to_rows[engine_move[3]], gs.files_to_cols[engine_move[2]]), gs.board)
