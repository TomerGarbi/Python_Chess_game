import sys
import time
import chess
from stockfish import Stockfish
import button
import pygame
pygame.init()


WIDTH, HEIGHT = 512, 512
dim = 8
square_size = HEIGHT // dim
FPS = 20
clock = pygame.time.Clock()
images = {}
font = pygame.font.SysFont('Arial', 16)
big_font = pygame.font.SysFont('Arial', 42)
engine = Stockfish(path="./stockfish_14.1_win_x64_avx2.exe")
engine.set_depth(12)
colors = {"black": (0, 0, 0), "white": (255, 255, 255), "orange": (255, 100, 20), "gray": (160, 160, 160),
          "light blue": (0, 191, 255), "off white": (245, 245, 210)}
sounds = {"move": pygame.mixer.Sound("sounds/move.mp3"), "castle": pygame.mixer.Sound("sounds/castle.mp3"),
          "capture": pygame.mixer.Sound("sounds/capture.mp3"), "check": pygame.mixer.Sound("sounds/check.mp3")}


def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ",
              "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    images["logo"] = pygame.transform.scale(
        pygame.image.load("./img/chess_game_icon.png"), (200, 200))
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(
            f"./img/Pieces/{piece}.png"), (square_size, square_size))
    images["gray_dot"] = pygame.transform.scale(
        pygame.image.load("./img/gray_dot.png"), (square_size, square_size))
    images["gray_circle"] = pygame.transform.scale(
        pygame.image.load("./img/gray_circle.png"), (square_size, square_size))


def draw_board(screen):
    for r in range(dim):
        for c in range(dim):
            color = colors["white"] if (r+c) % 2 == 0 else colors["gray"]
            pygame.draw.rect(screen, color, pygame.Rect(
                c * square_size, r * square_size, square_size, square_size))


def draw_pieces(screen, board):
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], pygame.Rect(
                    c * square_size, r * square_size, square_size, square_size))


def play_sound(gs: chess.GameState, move: chess.Move):
    if move.castle_move:
        sounds["castle"].play()
    elif gs.in_check():
        sounds["check"].play()
    elif move.piece_captured != "--":
        sounds["capture"].play()
    else:
        sounds["move"].play()



def draw_possible_piece_moves(moves, screen, gs):
    for move in moves:
        r, c = (move.end_row, move.end_col)
        if gs.board[r][c] == "--":
            pygame.draw.circle(screen, colors["light blue"], ((
                c + 0.5) * square_size, (r + 0.5) * square_size), square_size/6)
        else:
            pygame.draw.circle(screen, colors["light blue"], ((
                c + 0.5) * square_size, (r + 0.5) * square_size), square_size/2.25, 5)


def draw_square_selected(screen, square_selected):
    if square_selected != ():
        r, c = square_selected
        pygame.draw.rect(screen, colors["light blue"], pygame.Rect(
            c * square_size, r * square_size, square_size, square_size), 2)


def draw_game_state(screen, gs, possible_piece_moves, square_selected):
    draw_board(screen)
    draw_possible_piece_moves(possible_piece_moves, screen, gs)
    draw_pieces(screen, gs.board)
    draw_square_selected(screen, square_selected)


def get_piece_moves(r, c, valid_moves):
    moves = []
    for move in valid_moves:
        if move.start_row == r and move.start_col == c:
            moves.append(move)
    return moves


def wait_for_promotion(screen, gs, move):
    color = move.piece_moved[0]
    if color == "w":
        r, c = move.end_row * square_size, move.end_col * square_size
    else:
        r, c = move.end_row * square_size - 4 * square_size, move.end_col * square_size
    queen_button = button.Button(
        square_size, square_size, colors["white"], (c, r), "", "Q")
    rook_button = button.Button(
        square_size, square_size, colors["white"], (c, r + square_size), "", "R")
    knight_button = button.Button(
        square_size, square_size, colors["white"], (c, r + 2 * square_size), "",  "N")
    bishop_button = button.Button(
        square_size, square_size, colors["white"], (c, r + 3 * square_size), "", "B")
    buttons = [queen_button, rook_button, knight_button, bishop_button]
    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for b in buttons:
                    if b.hover_button(mouse):
                        return b.return_value
        for b in buttons:
            if b.hover_button(mouse):
                pygame.draw.rect(screen, colors["orange"], pygame.Rect(
                    b.position[0], b.position[1], square_size, square_size))
            else:
                pygame.draw.rect(screen, colors["off white"], pygame.Rect(
                    b.position[0], b.position[1], square_size, square_size))
            screen.blit(images[f"{color}{b.return_value}"], pygame.Rect(
                b.position[0], b.position[1], square_size, square_size))
        pygame.display.update()
        clock.tick(FPS)


def open_screen(screen):
    middle = (screen.get_width() / 2, screen.get_height() / 2)
    buttons_size = (150, 50)
    button_vs_computer = button.Button(
        buttons_size[0], buttons_size[1], colors["gray"], (middle[0] - 75, middle[1] + 20), "vs computer", 1)
    button_two_players = button.Button(
        buttons_size[0], buttons_size[1], colors["gray"], (middle[0] - 75, middle[1] + 90), "two players", 2)
    buttons = [button_vs_computer, button_two_players]
    run_open_screen = True
    quit = False
    while run_open_screen:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame. QUIT:
                run_open_screen = False
                quit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                for b in buttons:
                    if b.hover_button(mouse):
                        return b.return_value
        screen.fill(colors["white"])
        screen.blit(images["logo"], pygame.Rect(
            middle[0] - 100, middle[1] - 200, 200, 200))
        for b in buttons:
            if b.hover_button(mouse):
                pygame.draw.rect(screen, colors["orange"], pygame.Rect(
                    b.position[0], b.position[1], b.height, b.width))
            else:
                pygame.draw.rect(screen, b.color, pygame.Rect(
                    b.position[0], b.position[1], b.height, b.width))
            screen.blit(font.render(
                b.text, True, colors["black"]), (b.position[0] + 32, b.position[1] + 15))
        pygame.display.update()
        clock.tick(FPS)

    if quit:
        pygame.quit()
        return 0
    return -1


def game_end_screen(screen, gs, result):
    results = ["The Game Ended with a Draw",
               "White Won the Game", "Black Won the Game"]
    main_menu_button = button.Button(
        150, 50, colors["gray"], (200, 200), "main menu", "main_menu")
    buttons = [main_menu_button]
    draw_end_screen = True
    while draw_end_screen:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                draw_end_screen = False
                pygame.quit()
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                for b in buttons:
                    if b.hover_button(mouse):
                        main()
        screen.fill(colors["white"])
        screen.blit(big_font.render(
            results[result], True, colors["black"]), (50, 100))
        for b in buttons:
            if b.hover_button(mouse):
                pygame.draw.rect(screen, colors["orange"], pygame.Rect(
                    b.position[0], b.position[1], b.height, b.width))
            else:
                pygame.draw.rect(screen, b.color, pygame.Rect(
                    b.position[0], b.position[1], b.height, b.width))
            screen.blit(font.render(
                b.text, True, colors["black"]), (b.position[0] + 32, b.position[1] + 15))

        pygame.display.update()


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    gs = chess.GameState()
    load_images()
    option = open_screen(screen)
    if option == 1:
        result = play_vs_computer("b", screen, gs)
    elif option == 2:
        result = two_players_mode(screen, gs)
    time.sleep(0.5)
    game_end_screen(screen, gs, result)
    pygame.quit()


def engine_move_to_Move(engine_move, gs):
    return chess.Move((gs.ranks_to_rows[engine_move[1]], gs.files_to_cols[engine_move[0]]), (gs.ranks_to_rows[engine_move[3]], gs.files_to_cols[engine_move[2]]), gs.board)


def play_vs_computer(computer_color, screen, gs):
    run = True
    square_selected = ()
    players_clicks = []
    possible_piece_moves = []
    valid_moves = gs.get_valid_moves()
    move_made = False
    engine.set_elo_rating(700)
    while run:
        if gs.checkmate:
            run = False
            if gs.white_to_move:
                return 2
            else:
                return 1
        if gs.stalemate or gs.pawn_or_captures > 49:
            run = False
            return -1
        if gs.turn_color() == computer_color:
            m = engine.get_best_move()
            computer_move = engine_move_to_Move(m, gs)
            gs.make_move(valid_moves[valid_moves.index(computer_move)])
            play_sound(gs, gs.move_log[-1])
            valid_moves = gs.get_valid_moves()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return -1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // square_size
                row = location[1] // square_size
                if len(players_clicks) == 0:  # player's first click
                    if gs.board[row][col] != "--":
                        possible_piece_moves = get_piece_moves(
                            row, col, valid_moves)
                    else:  # player clicked on empty square
                        pass
                    square_selected = (row, col)
                    players_clicks.append(square_selected)
                elif len(players_clicks) == 1:  # player's second click
                    if (row, col) == square_selected:  # player clicked same square twice
                        square_selected = ()
                        players_clicks = []
                        possible_piece_moves = []
                    else:  # player clicked different square
                        players_clicks.append((row, col))
                        # try to make move
                        move = chess.Move(
                            players_clicks[0], players_clicks[1], gs.board, user_move=True)
                        if move in valid_moves:
                            move = valid_moves[valid_moves.index(move)]
                            move.user_move = True
                            if move.is_promotion:
                                move.promotion_choice = wait_for_promotion(
                                    screen, gs, move)
                            gs.make_move(move)
                            move_made = True
                            players_clicks = []
                            square_selected = ()
                        else:  # move is not valid:
                            # player clicked different piece
                            if gs.board[row][col][0] == gs.turn_color():
                                square_selected = (row, col)
                                players_clicks = [square_selected]
                                possible_piece_moves = get_piece_moves(
                                    row, col, valid_moves)
                            else:
                                players_clicks.pop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undo_move()
                    square_selected = ()
                    move_made = True
        if move_made:
            play_sound(gs, gs.move_log[-1])
            valid_moves = gs.get_valid_moves()
            fen = gs.FEN()
            engine.set_fen_position(fen)
            move_made = False
            possible_piece_moves = []
        draw_game_state(screen, gs, possible_piece_moves, square_selected)
        clock.tick(FPS)
        pygame.display.flip()


def two_players_mode(screen, gs):
    run = True
    square_selected = ()
    players_clicks = []
    possible_piece_moves = []
    valid_moves = gs.get_valid_moves()
    move_made = False
    while run:
        if gs.checkmate:
            run = False
            if gs.white_to_move:
                return 2
            else:
                return 1
        if gs.stalemate or gs.pawn_or_captures > 49:
            run = False
            return 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return -1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // square_size
                row = location[1] // square_size
                if len(players_clicks) == 0:  # player's first click
                    if gs.board[row][col] != "--":
                        possible_piece_moves = get_piece_moves(
                            row, col, valid_moves)
                    else:  # player clicked on empty square
                        pass
                    square_selected = (row, col)
                    players_clicks.append(square_selected)
                elif len(players_clicks) == 1:  # player's second click
                    if (row, col) == square_selected:  # player clicked same square twice
                        square_selected = ()
                        players_clicks = []
                        possible_piece_moves = []
                    else:  # player clicked different square
                        players_clicks.append((row, col))
                        # try to make move
                        move = chess.Move(
                            players_clicks[0], players_clicks[1], gs.board, user_move=True)
                        if move in valid_moves:
                            move = valid_moves[valid_moves.index(move)]
                            move.user_move = True
                            if move.is_promotion:
                                move.promotion_choice = wait_for_promotion(
                                    screen, gs, move)
                            gs.make_move(move)
                            move_made = True
                            players_clicks = []
                            square_selected = ()
                        else:  # move is not valid:
                            # player clicked different piece
                            if gs.board[row][col][0] == gs.turn_color():
                                square_selected = (row, col)
                                players_clicks = [square_selected]
                                possible_piece_moves = get_piece_moves(
                                    row, col, valid_moves)
                            else:
                                players_clicks.pop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undo_move()
                    square_selected = ()
                    move_made = True
        if move_made:
            if len(gs.move_log) > 0:
                play_sound(gs, gs.move_log[-1])
            valid_moves = gs.get_valid_moves()
            fen = gs.FEN()
            engine.set_fen_position(fen)
            possible_piece_moves = []
            move_made = False
        draw_game_state(screen, gs, possible_piece_moves, square_selected)
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
