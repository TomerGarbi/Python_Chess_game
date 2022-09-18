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
        images[piece] = pygame.transform.scale(pygame.image.load(f"./Pieces/{piece}.png"), (square_size, square_size))


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


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)



def main():
    screen = pygame.display.set_mode((WIDTH, HIGHT))
    clock = pygame.time.Clock()
    gs = chess.GameState()
    load_images()
    run = True
    square_selected = ()
    players_clicks = []
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
                if square_selected == (row, col):   # user clicked same square twice
                    square_selected = ()
                    players_clicks = []
                elif gs.board[row][col] == "--" and len(players_clicks) == 0: #   user first click is empty square
                    pass
                else:
                    square_selected = (row, col)
                    players_clicks.append(square_selected)
                if len(players_clicks) == 2:    #   player may have made a valid move
                    move = chess.Move(players_clicks[0], players_clicks[1], gs.board)
                    if move in valid_moves:
                        print(move.get_chess_notation())
                        gs.make_move(move)
                        move_made = True
                    square_selected = ()
                    players_clicks = []
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs)
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
