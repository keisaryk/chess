from Table_chess import Table
from assisting_functions import get_move, get_player

TIE_NOTICE = 'a tie!'


def game(first_table):
    counter = 0

    while first_table.is_player_can_move(get_player(counter)):
        player = get_player(counter)
        if first_table.is_king_threated(player):
            print(f'{player} is in chess')
        print(f'now it is {player} move')
        src_col, src_row, dst_col, dst_row = get_move()
        counter, tool, a, b, c = first_table.move(src_col, src_row, dst_col, dst_row, player, counter)
        print(first_table)
    return get_player(counter)


def end_game(first_table, last_turn_player):
    if first_table.is_king_threated(last_turn_player):
        print(f'{last_turn_player} lose the game!')
    else:
        print(TIE_NOTICE)


def main():
    first_table = Table()
    first_table.start_table()
    print(first_table)
    end_game(first_table, game(first_table))


if __name__ == '__main__':
    main()
