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
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_game_state(screen, gs)
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
