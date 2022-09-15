import sys

import pygame
pygame.init()

WIDTH, HIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HIGHT))
pygame.display.set_caption("hello")
FPS = 30

def main():
    run = True
    counter = 0;
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
    print(counter)
    sys.exit()




if __name__ == "__main__":
    main()
