from Table_chess import Table
from assisting_functions import get_move, get_player
from Tools_chess import King, Pion
from main_functions import game, end_game

TIE_NOTICE = 'a tie!'


def test_pion_to_new_tool():
    test_table = Table()
    test_table.matrix[6][0] = King('w')
    test_table.matrix[1][0] = King('b')
    test_table.matrix[6][5] = Pion('w')
    print(test_table)
    end_game(test_table, game(test_table))


def test_chess_mate():
    test_table = Table()
    test_table.start_table()
    counter = 0
    test_table.make_move(5, 1, 5, 2)
    test_table.make_move(4, 6, 4, 5)
    test_table.make_move(6, 1, 6, 3)
    test_table.make_move(3, 7, 7, 3)
    print(test_table)

    end_game(test_table, game(test_table))


def test_castlite():
    test_table = Table()
    test_table.start_table()
    counter = 0
    test_table.tset_castle_start()
    print(test_table)

    end_game(test_table, game(test_table))


if __name__ == '__main__':
    test_pion_to_new_tool()