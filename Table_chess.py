from Tools_chess import Pion, Knight, King, Rook, Queen, Bishop
from assisting_functions import is_castlite, get_squeres_in_way, get_threated_place, get_new_tool
import copy

START_LINE_WHITE_INDEX = 0
START_LINE_BLACK_INDEX = 7
PION_LINE_WHITE_INDEX = 1
PION_LINE_BLACK_INDEX = 6
AMOUNT_OF_COLS = 8
AMOUNT_OF_ROWS = 8
START_LINE_WHITE = [Rook('w'), Knight('w'), Bishop('w'), King('w'), Queen('w'), Bishop('w'), Knight('w'), Rook('w')]
START_LINE_BLACK = [Rook('b'), Knight('b'), Bishop('b'), King('b'), Queen('b'), Bishop('b'), Knight('b'), Rook('b')]
WHITE_PION_ROW = [Pion('w') for i in range(AMOUNT_OF_COLS)]
BLACK_PION_ROW = [Pion('b') for j in range(AMOUNT_OF_COLS)]
OUTSIDE_TABLE_ROW = '\n      A    B    C    D    E    F    G    H'
NOT_VALID_SRC_DST_NOTICE ='not valid move, src or dst is not according to the rules'
NOT_VALID_MOVE_NOTICE ='not valid move, the tool you choose cant do that move'
KING_THREATED_NOTICE = 'not valid move, king is under threat'


class Table(object):
    def __init__(self):
        """
        receives Table object
        define its matrix (8 * 8)
        :returns None
        """
        self.matrix = [['-' for i in range(AMOUNT_OF_COLS)] for j in range(AMOUNT_OF_ROWS)]
        self.white_king_threated = False
        self.black_king_threated = False

    def start_table(self):
        """
        receives Table object
        makes the Table matrix ready for start game
        :returns: None
        """
        self.matrix[START_LINE_WHITE_INDEX] = START_LINE_WHITE
        self.matrix[PION_LINE_WHITE_INDEX] = WHITE_PION_ROW
        self.matrix[START_LINE_BLACK_INDEX] = START_LINE_BLACK
        self.matrix[PION_LINE_BLACK_INDEX] = BLACK_PION_ROW

    def __str__(self):
        """
        receives Table object
        makes visual chess board str
        :returns:  str of the board
        """
        matrix_to_print = []
        for row in range(AMOUNT_OF_ROWS):
            matrix_to_print.append(row+1)
            matrix_to_print.append([])
            for squere in self.matrix[row]:
                matrix_to_print[-1].append(str(squere))
        str_to_print = str(matrix_to_print)[1:-1]
        str_to_print = str_to_print.replace('],', ']\n').replace('1,', ' 1,')
        return str_to_print + OUTSIDE_TABLE_ROW

    def move(self, src_col, src_row, dst_col, dst_row, player, counter):
        """
        :param src_col: int 0-7
        :param src_row: int 0-7
        :param dst_col: int 0-7
        :param dst_row: int 0-7
        :param player: str 'w' or 'b'
        :param counter: int
        checks move and do it if it is legal
        :return: counter: int
        """
        if not self.check_valid_src_dst(src_col, src_row, dst_col, dst_row, player):
            print(NOT_VALID_SRC_DST_NOTICE)
            return counter, NOT_VALID_SRC_DST_NOTICE, None, None, None, None

        now_playing_tool = self.get_tool(src_col, src_row)

        if not self.check_valid_tool_move(src_col, src_row, dst_col, dst_row, player, now_playing_tool):
            print(NOT_VALID_MOVE_NOTICE)
            return counter, NOT_VALID_MOVE_NOTICE, None, None, None, None
        else:
            new_table = Table()
            new_table.matrix = copy.deepcopy(self.matrix)
            castle, new_tool = new_table.make_move(src_col, src_row, dst_col, dst_row, is_castlite(now_playing_tool, src_col, dst_col))

            if new_table.is_king_threated(player):
                print(KING_THREATED_NOTICE)
                return counter, KING_THREATED_NOTICE, None, None, None, None
            else:
                self.matrix = new_table.matrix
                tool = self.get_tool(dst_col, dst_row)
                if type(tool) == King:
                    tool.did_king_move = True
                if type(tool) == Rook:
                    tool.did_rook_move = True

            if castle is not None:
                print(castle)
                return counter + 1, (src_col, src_row), (dst_col, dst_row), castle[0], castle[1], None

            if new_tool is not None:
                return counter + 1, (src_col, src_row), (dst_col, dst_row), None, None, new_tool

            return counter + 1, (src_col, src_row), (dst_col, dst_row), None, None, None

    def test_move(self, src_col, src_row, dst_col, dst_row, player):
        """
        :param src_col: int 0-7
        :param src_row: int 0-7
        :param dst_col: int 0-7
        :param dst_row: int 0-7
        :param player: str 'w' or 'b'
        checks if move is valid
        :return: bool
        """
        if not self.check_valid_src_dst(src_col, src_row, dst_col, dst_row, player):
            return False

        now_playing_tool = self.get_tool(src_col, src_row)

        if not self.check_valid_tool_move(src_col, src_row, dst_col, dst_row, player, now_playing_tool):
            return False
        else:
            new_table = Table()
            new_table.matrix = copy.deepcopy(self.matrix)
            new_table.make_move(src_col, src_row, dst_col, dst_row)
            if new_table.is_king_threated(player):
                return False
        return True

    def get_tool(self, col, row):
        """
        :param col: int
        :param row: int
        finds the tool in that position in the Table
        (if there is one) and returns it
        :return: bool or Tool chess object
        """
        if self.matrix[row][col] == '-':
            return None
        return self.matrix[row][col]

    def check_valid_src_dst(self, src_col, src_row, dst_col, dst_row, player):
        """
        receives Table
        :param src_col: int 0-7
        :param src_row: int 0-7
        :param dst_col: int 0-7
        :param dst_row: int 0-7
        :param player: str 'w' or 'b'
        checks if src and dst of the move are valid
        :return: bool
        """
        valid_src = self.check_valid_src(src_col, src_row, player)
        valid_dst = self.check_valid_dst(dst_col, dst_row, player)
        is_move = (src_col, src_row) != (dst_col, dst_row)
        return valid_src and valid_dst and is_move

    def make_move(self, src_col, src_row, dst_col, dst_row, is_castlite=False):
        """
        :param src_col: int 0-7
        :param src_row: int 0-7
        :param dst_col: int 0-7
        :param dst_row: int 0-7
        makes move in the Table
        :return: None
        """
        tool = self.get_tool(src_col, src_row)
        self.matrix[dst_row][dst_col] = tool
        self.matrix[src_row][src_col] = '-'
        if is_castlite:
            if dst_col - src_col == -2:
                self.matrix[src_row][src_col-1] = self.get_tool(src_col-3, src_row)
                self.matrix[src_row][src_col-3] = '-'
                return ((src_col-3, src_row), (src_col-1, src_row)), self.get_tool(src_col-3, src_row)
            else:
                self.matrix[src_row][src_col+1] = self.get_tool(src_col+4, src_row)
                self.matrix[src_row][src_col+4] = '-'
                return ((src_col+4, src_row), (src_col+1, src_row)), self.get_tool(src_col+4, src_row)

        if type(tool) == Pion and dst_row in (0, 7):
            self.matrix[dst_row][dst_col] = get_new_tool(tool.team)
            return None, self.get_tool(dst_col, dst_row)

        return None, None


    def is_tool_not_in_the_way(self, src_col, src_row, dst_col, dst_row):
        """checks if there is tool in the way from src to dst"""
        if type(self.get_tool(src_col, src_row)) == Knight:
            return True
        for col, row in get_squeres_in_way(src_col, src_row, dst_col, dst_row):
            if self.matrix[row][col] != '-':
                return False
        return True

    def check_valid_tool_move(self, src_col, src_row, dst_col, dst_row, player, playing_tool):
        """
        :param src_col: int 0-7
        :param src_row: int 0-7
        :param dst_col: int 0-7
        :param dst_row: int 0-7
        :param player: str 'w' or 'b'
        check if the move is valid
        :return: bool
        """
        if not self.is_tool_not_in_the_way(src_col, src_row, dst_col, dst_row):
            return False

        return self.check_valid_tool_moving(src_col, src_row, dst_col, dst_row, playing_tool) or\
            self.check_valid_tool_eat(src_col, src_row, dst_col, dst_row, player, playing_tool) or\
            self.check_valid_castlite(src_col, src_row, dst_col, dst_row, playing_tool)

    def check_valid_tool_eat(self, src_col, src_row, dst_col, dst_row, player, playing_tool):
        """
        :param src_col: int 0-7
        :param src_row: int 0-7
        :param dst_col: int 0-7
        :param dst_row: int 0-7
        :param player: str 'w' or 'b'
        :param playing_tool: tool object
        check if the move is a valid tool eating
        :return: bool
        """
        enemy_tool = self.get_tool(dst_col, dst_row)
        if enemy_tool == None:
            return False
        if enemy_tool.team != player:
            return (dst_col - src_col, dst_row - src_row) in playing_tool.threat()
        return False

    def check_valid_castlite(self, src_col, src_row, dst_col, dst_row, tool):
        if is_castlite(tool, src_col, dst_col) and src_row == dst_row and\
                not self.get_threat_king_status(tool.team):
            if not tool.did_king_move:
                try:
                    if dst_col == 5:
                        if not self.get_tool(7, src_row).did_rook_move and not self.is_place_threated(src_row, 5, tool.team):
                            return True
                    if dst_col == 1:
                        if not self.get_tool(0, src_row).did_rook_move and not self.is_place_threated(src_row, 2, tool.team):
                            return True
                except AttributeError:
                    return False

    def is_king_threated(self, team):
        """
        receives move
        check if king is threated after the move
        return true if it is (else False)
        """
        king_place = self.find_king(team)
        for row in range(AMOUNT_OF_ROWS):
            for col in range(AMOUNT_OF_COLS):
                if self.matrix[row][col] != '-':
                    tool = self.matrix[row][col]
                    if tool.team != team:
                        threated_places = get_threated_place(col, row, tool)
                        if king_place in threated_places and self.is_tool_not_in_the_way(col, row, king_place[0], king_place[1]):
                            self.change_threat_king(team, True)
                            return True
        self.change_threat_king(team, False)
        return False

    def find_king(self, team):
        """
        :param team: str 'w' or 'b'
        finds the king of gotten team
        :return: tuple, (int, int) - place of the king
        """
        for row in range(AMOUNT_OF_ROWS):
            for squere in range(AMOUNT_OF_COLS):
                tool = self.matrix[row][squere]
                if type(tool) == King and tool.team == team:
                    return squere, row

    def check_valid_src(self, src_col, src_row, player):
        """
        receives src, dst, player
        check if there is tool in src and if it belongs the player
        if it is returns True
        """
        try:
            tool = self.get_tool(src_col, src_row)
            if tool.team == player:
                return True
            else:
                return False
        except AttributeError:
            return False

    def check_valid_dst(self, dst_col, dst_row, player):
        """
        :param dst_col: int 0-7
        :param dst_row: int 0-7
        :param player: str 'w' or 'b'
        :return: bool
        """
        if self.get_tool(dst_col, dst_row) == None or self.get_tool(dst_col, dst_row).team != player:
            return True

    def is_player_can_move(self, team):
        """
        :param: team: str
        checks if player can move
        :return: bool
        """
        check_table = Table()
        check_table.matrix = copy.deepcopy(self.matrix)
        for src_col in range(AMOUNT_OF_COLS):
            for src_row in range(AMOUNT_OF_ROWS):
                if check_table.get_tool(src_col, src_row) != None:
                    for dst_col in range(AMOUNT_OF_COLS):
                        for dst_row in range(AMOUNT_OF_ROWS):
                            if check_table.test_move(src_col, src_row, dst_col, dst_row, team):
                                return True
        return False

    def get_threat_king_status(self, team):
        if team == 'w':
            return self.white_king_threated
        return self.black_king_threated

    def change_threat_king(self, team, value):
        if team == 'w':
            self.white_king_threated = value
        else:
            self.black_king_threated = value

    def check_tool_options(self, tool, src_row):
        """
        :param: src_col: int 0-7
        :param src_row: int 0-7
        finds tool in this position and get its optional moves
        :return: list of optional moves
        """
        return tool.optional_move(src_row)

    def check_valid_tool_moving(self, src_col, src_row, dst_col, dst_row, playing_tool):
        """
        :param src_col: int 0-7
        :param src_row: int 0-7
        :param dst_col: int 0-7
        :param dst_row: int 0-7
        check if the move is a valid tool moving
        :return: bool
        """
        return (dst_col - src_col, dst_row - src_row) in self.check_tool_options(playing_tool, src_row) and\
    self.get_tool(dst_col, dst_row) is None

    def tset_castle_start(self):
        self.matrix[0] = [Rook('w'), '-', '-', King('w'), '-', Bishop('w'), Knight('w'), Rook('w')]
        self.matrix[7] = [Rook('b'), Knight('b'), Bishop('b'), Queen('b'), King('b'), '-', '-', Rook('b')]

    def is_place_threated(self, row, col, team):
        for op_row in range(AMOUNT_OF_ROWS):
            for op_col in range(AMOUNT_OF_COLS):
                if self.matrix[op_row][op_col] != '-':
                    tool = self.matrix[op_row][op_col]
                    if tool.team != team:
                        threated_places = get_threated_place(op_col, op_row, tool)
                        if (col, row) in threated_places and self.is_tool_not_in_the_way(op_col, op_row, col, row):
                            return True
        return False
# assisting functions
