import sys
import chess
import pygame
pygame.init()

WIDTH, HIGHT = 512, 512
dim = 8
square_size = HIGHT // dim
FPS = 15
images = {}


def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
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
            pygame.draw.circle(screen, (0, 0, 100), ((c + 0.5) * square_size, (r + 0.5) * square_size), square_size/6)
        else:
            pygame.draw.circle(screen, (0, 0, 100), ((c + 0.5) * square_size, (r + 0.5) * square_size), square_size/2.25, 5)


def draw_game_state(screen, gs, possible_piece_moves):
    draw_board(screen)
    draw_pieces(screen, gs.board)
    draw_possible_piece_moves(possible_piece_moves, screen, gs)



def get_piece_moves(r, c, valid_moves):
    moves = []
    for move in valid_moves:
        if move.start_row == r and move.start_col == c:
            moves.append(move)
    return moves


def main():
    screen = pygame.display.set_mode((WIDTH, HIGHT))
    clock = pygame.time.Clock()
    gs = chess.GameState()
    load_images()
    run = True
    square_selected = ()
    players_clicks = []
    possible_piece_moves = []
    valid_moves = gs.get_valid_moves()
    move_made = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // square_size
                row = location[1] // square_size
                if len(players_clicks) == 0: # player's first click
                    if gs.board[row][col] != "--":
                        possible_piece_moves = get_piece_moves(row, col, valid_moves)
                        print([m.get_chess_notation() for m in  possible_piece_moves])
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
                        move = chess.Move(players_clicks[0], players_clicks[1], gs.board)
                        if move in valid_moves:
                            gs.make_move(move)
                            move_made = True
                            players_clicks = []
                            square_selected = ()
                        else: #  move is not valid:
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
            valid_moves = gs.get_valid_moves()
            possible_piece_moves = []
            move_made = False

        draw_game_state(screen, gs, possible_piece_moves)
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
