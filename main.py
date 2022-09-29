import sys
import chess
import pygame
pygame.init()

WIDTH, HIGHT = 512, 512
dim = 8
square_size = HIGHT // dim
FPS = 15
clock = pygame.time.Clock()
images = {}
font = pygame.font.SysFont('Arial', 16)

def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    images["logo"] = pygame.transform.scale(pygame.image.load("./img/chess_game_icon.png"), (200, 200))
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f"./img/Pieces/{piece}.png"), (square_size, square_size))
    images["gray_dot"] = pygame.transform.scale(pygame.image.load("./img/gray_dot.png"), (square_size, square_size))
    images["gray_circle"] = pygame.transform.scale(pygame.image.load("./img/gray_circle.png"), (square_size, square_size))


def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("grey")]
    for r in range(dim):
        for c in range(dim):
            color = colors[(r+c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c * square_size, r * square_size, square_size, square_size))


def draw_pieces(screen, board):
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], pygame.Rect(c * square_size, r * square_size, square_size, square_size))


def draw_possible_piece_moves(moves, screen, gs):
    for move in moves:
        r, c = (move.end_row, move.end_col)
        if gs.board[r][c] == "--":
            # screen.blit(images["gray_dot"], pygame.Rect(c * square_size, r * square_size, square_size, square_size))
            pygame.draw.circle(screen, (0, 191, 255), ((c + 0.5) * square_size, (r + 0.5) * square_size), square_size/6)
        else:
            pygame.draw.circle(screen, (0, 191, 255), ((c + 0.5) * square_size, (r + 0.5) * square_size), square_size/2.25, 5)


def draw_game_state(screen, gs, possible_piece_moves,):
    draw_board(screen)
    draw_possible_piece_moves(possible_piece_moves, screen, gs)
    draw_pieces(screen, gs.board)


def get_piece_moves(r, c, valid_moves):
    moves = []
    for move in valid_moves:
        if move.start_row == r and move.start_col == c:
            moves.append(move)
    return moves


def wait_for_promotion_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "Q"
                elif event.key == pygame.K_n:
                    return "N"
                elif event.key == pygame.K_r:
                    return "R"
                elif event.key == pygame.K_b:
                    return "B"
                else:
                    print("press 'q', 'r', 'n' or 'b'")
        clock.tick(FPS)

#
# def draw_open_screen(screen):
#     pygame.display.

def open_screen(screen):
    buttons_size = (150, 50)
    start_button_pos = (-75 + screen.get_width() // 2, -10 + screen.get_height() // 2)
    run_open_screen = True
    quit = False
    while run_open_screen:
        screen.fill((255, 255, 255))
        location = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame. QUIT:
                run_open_screen = False
                quit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_pos[0] <= location[0] <= start_button_pos[0] + buttons_size[0] and start_button_pos[1] <= location[1] <= buttons_size[1] + start_button_pos[1]:
                    return 2
        screen.blit(images["logo"], pygame.Rect(150, 25, 200, 200))
        pygame.draw.rect(screen, (125, 125, 125), pygame.Rect(start_button_pos[0], start_button_pos[1], buttons_size[0], buttons_size[1]))
        screen.blit(font.render('Start Game', True, (0, 0, 0)), (start_button_pos[0] + 32, start_button_pos[1] + 15))
        pygame.display.update()
        clock.tick(FPS)
    if quit:
        pygame.quit()
        return 0
    return 1





def main():
    screen = pygame.display.set_mode((WIDTH, HIGHT))
    gs = chess.GameState()
    load_images()
    run = True
    square_selected = ()
    players_clicks = []
    possible_piece_moves = []
    valid_moves = gs.get_valid_moves()
    move_made = False
    start_game = open_screen(screen)
    if start_game == 0:
        exit(0)

    while run:
        if gs.checkmate:
            run = False
            if gs.white_to_move:
                print("black is the winner")
            else:
                print("white winner")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // square_size
                row = location[1] // square_size
                if len(players_clicks) == 0:    # player's first click
                    if gs.board[row][col] != "--":
                        possible_piece_moves = get_piece_moves(row, col, valid_moves)
                    else:   # player clicked on empty square
                        pass
                    square_selected = (row, col)
                    players_clicks.append(square_selected)
                elif len(players_clicks) == 1:      # player's second click
                    if (row, col) == square_selected: # player clicked same square twice
                        square_selected = ()
                        players_clicks = []
                        possible_piece_moves = []
                    else:   # player clicked different square
                        players_clicks.append((row, col))
                        # try to make move
                        move = chess.Move(players_clicks[0], players_clicks[1], gs.board, user_move=True)
                        if move in valid_moves:
                            move = valid_moves[valid_moves.index(move)]
                            move.user_move = True
                            if move.is_promotion:
                                move.promotion_choice = wait_for_promotion_key()
                            gs.make_move(move)
                            move_made = True
                            players_clicks = []
                            square_selected = ()
                        else:   # move is not valid:
                            if gs.board[row][col][0] == gs.turn_color():    # player clicked different piece
                                square_selected = (row, col)
                                players_clicks = [square_selected]
                                possible_piece_moves = get_piece_moves(row, col, valid_moves)
                            else:
                                players_clicks.pop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undo_move()
                    move_made = True
        if move_made:
            for r in gs.castling_rights_log:
                print(r)
            print("-------------------------")
            valid_moves = gs.get_valid_moves()
            possible_piece_moves = []
            move_made = False
        draw_game_state(screen, gs, possible_piece_moves)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
