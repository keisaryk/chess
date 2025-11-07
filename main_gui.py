import time
import pygame
from assisting_functions import get_player
from Table_chess import Table
from Tools_chess import King, Queen, Rook, Bishop, Knight, Pion

TIE_NOTICE = 'a tie!'
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

dict_matrix_to_rect = {}
place_to_rect_image = {}
dict_tool_to_image = {}

pygame.init()

win = pygame.display.set_mode((400, 500))
win.fill((255, 255, 255))
pygame.display.set_caption("Chess Game")
font = pygame.font.Font('freesansbold.ttf', 32)


def show_backround():
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
            if y % 100 != 0:
                pygame.draw.rect(win, (0, 0, 0), (0, y, width, height))
            pygame.draw.rect(win, (255, 255, 255), (x, y, width, height))
            pygame.draw.rect(win, (0, 0, 0), (x+50, y, width, height))
            x += 100
        y += 50


def get_place_to_rect_dict():
    place_to_rect_image[(0, 0)] = pygame.image.load('pictures\white_rook.png')
    place_to_rect_image[(0, 1)] = pygame.image.load('pictures\white_knight.png')
    place_to_rect_image[(0, 2)] = pygame.image.load('pictures\white_bishop.png')
    place_to_rect_image[(0, 3)] = pygame.image.load('pictures\white_king.png')
    place_to_rect_image[(0, 4)] = pygame.image.load('pictures\white_queen.png')
    place_to_rect_image[(0, 5)] = pygame.image.load('pictures\white_bishop.png')
    place_to_rect_image[(0, 6)] = pygame.image.load('pictures\white_knight.png')
    place_to_rect_image[(0, 7)] = pygame.image.load('pictures\white_rook.png')
    place_to_rect_image[(7, 0)] = pygame.image.load('pictures\black_rook.png')
    place_to_rect_image[(7, 1)] = pygame.image.load('pictures\black_knight.png')
    place_to_rect_image[(7, 2)] = pygame.image.load('pictures\black_bishop.png')
    place_to_rect_image[(7, 3)] = pygame.image.load('pictures\black_king.png')
    place_to_rect_image[(7, 4)] = pygame.image.load('pictures\black_queen.png')
    place_to_rect_image[(7, 5)] = pygame.image.load('pictures\black_bishop.png')
    place_to_rect_image[(7, 6)] = pygame.image.load('pictures\black_knight.png')
    place_to_rect_image[(7, 7)] = pygame.image.load('pictures\black_rook.png')


def show_first_last_row():
    faze = 0
    counter = 0
    for tool in place_to_rect_image.values():
        if counter < 8:
            if counter == 3:
                y_faze = -10
            elif counter == 4:
                y_faze = -5
            else:
                y_faze = 0

            win.blit(tool, (10+faze, 0+y_faze))
        elif counter == 8:
            faze = 0
            win.blit(tool, (10 + faze, 350))
        else:
            win.blit(tool, (10+faze, 350))

        counter += 1
        faze += 50
        pygame.display.flip()


def show_pions():
    cc = 0
    for i in range(8):
        place_to_rect_image[(i, 1)] = pygame.image.load('pictures\white_pion.png')
        place_to_rect_image[(i, 6)] = pygame.image.load('pictures\black_pion.png')
        win.blit(place_to_rect_image[(i, 1)], (10+cc, 45))
        win.blit(place_to_rect_image[(i, 6)], (10+cc, 300))
        cc += 50
    pygame.display.flip()


def show_tools():
    get_place_to_rect_dict()
    show_first_last_row()
    show_pions()


def get_dict_tool_to_image():
    dict_tool_to_image[(Pion, 'w')] = pygame.image.load('pictures\white_pion.png')
    dict_tool_to_image[(Pion, 'b')] = pygame.image.load('pictures\black_pion.png')
    dict_tool_to_image[(King, 'w')] = pygame.image.load('pictures\white_king.png')
    dict_tool_to_image[(King, 'b')] = pygame.image.load('pictures\black_king.png')
    dict_tool_to_image[(Queen, 'w')] = pygame.image.load('pictures\white_queen.png')
    dict_tool_to_image[(Queen, 'b')] = pygame.image.load('pictures\black_queen.png')
    dict_tool_to_image[(Bishop, 'w')] = pygame.image.load('pictures\white_bishop.png')
    dict_tool_to_image[(Bishop, 'b')] = pygame.image.load('pictures\black_bishop.png')
    dict_tool_to_image[(Knight, 'w')] = pygame.image.load('pictures\white_knight.png')
    dict_tool_to_image[(Knight, 'b')] = pygame.image.load('pictures\black_knight.png')
    dict_tool_to_image[(Rook, 'w')] = pygame.image.load('pictures\white_rook.png')
    dict_tool_to_image[(Rook, 'b')] = pygame.image.load('pictures\black_rook.png')


def get_color_squere(place):
    if (place[0] + place[1]) % 2 == 0:
        return (255, 255, 255)
    else:
        return (0, 0, 0)


def move_tool_show(place, dst_col, dst_row, tool):
    src = dict_matrix_to_rect[place]
    dst = dict_matrix_to_rect[(dst_col, dst_row)]
    pygame.draw.rect(win, get_color_squere(place), (src[0]-10, src[1], 50, 50))
    pygame.draw.rect(win, get_color_squere((dst_col, dst_row)), (dst[0]-10, dst[1], 50, 50))
    place_to_rect_image[(dst_col, dst_row)] = dict_tool_to_image[(type(tool), tool.team)]

    win.blit(place_to_rect_image[(dst_col, dst_row)], dict_matrix_to_rect[(dst_col, dst_row)])
    pygame.display.flip()


def get_dict_rect():
    x = 10
    y = 0
    for row in range(8):
        for col in range(8):
            dict_matrix_to_rect[(col, row)] = (x, y)
            x += 50
        x = 10
        y += 50


def get_pos(x_pos):
    start_x = 0
    for j in range(8):
        if x_pos < start_x + 50 and start_x <= x_pos:
            return j
        start_x += 50
    return 7


def get_squere(pos):
    col = get_pos(pos[0])
    row = get_pos(pos[1])
    return col, row


def display_text(content, font=font):
    pygame.draw.rect(win, WHITE, (0, 400, 400, 100))
    text = font.render(content, True, GREEN, BLUE)
    text_rect = text.get_rect()
    text_rect.center = (200, 450)
    win.blit(text, text_rect)
    pygame.display.update()


def get_user_move():
    highlight = False
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == 1025:
                if highlight:
                    new_pos = pygame.mouse.get_pos()
                    return get_squere(pos), get_squere(new_pos)
                else:
                    pos = pygame.mouse.get_pos()
                highlight = not highlight


def game(first_table):
    counter = 0

    while first_table.is_player_can_move(get_player(counter)):
        player = get_player(counter)
        if first_table.is_king_threated(player):
            display_text(f'{player} is in chess')

        display_text(f'now it is {player} move')
        (src_col, src_row), (dst_col, dst_row) = get_user_move()
        try:
            counter, pos, new_pos, sec_pos, sec_new_pos, new_tool = first_table.move(src_col, src_row, dst_col, dst_row, player, counter)
        except ValueError:
            display_text('try again')

        if type(pos) is tuple:
            move_tool_show((src_col, src_row), dst_col, dst_row, first_table.get_tool(dst_col, dst_row))
        print(first_table)

        if type(pos) is str:
            display_text(pos, pygame.font.Font('freesansbold.ttf', 14))
            time.sleep(2)

        if sec_pos is not None:
            move_tool_show(sec_pos, sec_new_pos[0], sec_new_pos[1], first_table.get_tool(sec_new_pos[0], sec_new_pos[1]))

        if new_tool is not None:
            rect_pos = dict_matrix_to_rect[(dst_col, dst_row)]
            pygame.draw.rect(win, get_color_squere((dst_col, dst_row)), (rect_pos[0] - 10, rect_pos, 50, 50))
            place_to_rect_image[(dst_col, dst_row)] = dict_tool_to_image[type(new_tool)]
            win.blit(place_to_rect_image[dst_col, dst_row], dict_matrix_to_rect[(dst_col, dst_row)])
            pygame.display.flip()

    return get_player(counter)


def end_game(first_table, last_turn_player):
    if first_table.is_king_threated(last_turn_player):
        display_text(f'{last_turn_player} lose the game!')
    else:
        display_text(TIE_NOTICE)
    time.sleep(3)


def get_dicts():
    get_dict_rect()
    get_dict_tool_to_image()


def display_game():
    show_backround()
    show_tools()


def main():
    first_table = Table()
    first_table.start_table()
    get_dicts()
    display_game()
    print(first_table)
    end_game(first_table, game(first_table))


if __name__ == '__main__':
    main()

