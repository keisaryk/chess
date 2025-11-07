import pygame
import time

pygame.init()

win = pygame.display.set_mode((400, 400))

pygame.display.set_caption("Chess Game")
# pygame.mouse.get_pressed()

x = 0
y = 0
width = 50
height = 50
vel = 5

for j in range(8):
    if j % 2 == 0:
        x = 0
    else:
        x = 50
    for i in range(5):
        pygame.draw.rect(win, (255, 255, 255), (x, y, width, height))
        x += 100
    y += 50

a = pygame.draw.rect(win, (255, 0, 0), (20, 20, 20, 20))
pions = pygame.image.load(r"C:\Users\yuval\OneDrive\שולחן העבודה\אסק\מתנה\pion_white_and_black.png")

win.blit(pions, (20, 20))
# pygame.display.update()
pygame.display.flip()
pions.fill((255, 255, 255, 0))
win.blit(pions, (100, 100))
pygame.draw.rect(pions, (255, 255, 255, 0), (40, 40, 100, 100))
pygame.display.update()
pygame.display.flip()

def get_pos(x_pos):
    start_x = 0
    for j in range(8):
        if x_pos < start_x + 50 and start_x < x_pos:
            return j
        start_x += 50


def get_squere(pos):
    col = get_pos(pos[0])
    row = get_pos(pos[1])
    return col, row





def get_move():
    while True:
        highlight = False
        for event in pygame.event.get():
            if event.type == 1025:
                if highlight:
                    print(highlight)
                    new_pos = pygame.mouse.get_pos()
                    return get_squere(pos), get_squere(new_pos)
                else:
                    pos = pygame.mouse.get_pos()
                highlight = not highlight

"""
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    src, dst = get_move()
    print(src, dst)"""

get_move()