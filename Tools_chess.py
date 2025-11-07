KNIGHT_MOVE_THREAT = [(i, j) for i in [1, -1] for j in [2, -2]] + [(i, j) for i in [2, -2] for j in [1, -1]]
ROOK_MOVE_DIRECTION = [(1, 0), (0, -1), (-1, 0), (0, 1)]
BISHOP_MOVE_DIRECTION = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
QUEEN_MOVE_DIRECTION = [(1, 0), (0, -1), (-1, 0), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

optional_move_and_threat_king = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
optional_move_and_threat_king.remove((0, 0))


def get_tool_move_option(tool_move_direction):
    """
    :param: tool_move_direction: list
    :return: list of all move options of the tool
    """
    tool_move_options = []
    for direction in tool_move_direction:
        for num_sqr in range(1, 8):
            tool_move_options.append((direction[0] * num_sqr, direction[1] * num_sqr))
    return tool_move_options


rook_move_option = get_tool_move_option(ROOK_MOVE_DIRECTION)
bishop_move_option = get_tool_move_option(BISHOP_MOVE_DIRECTION)
queen_move_option = get_tool_move_option(QUEEN_MOVE_DIRECTION)


class Pion(object):
    def __init__(self, team):
        if team in ['w', 'b']:
            self.team = team
        else:
            print('team got to be w or b')
            raise AttributeError

    def optional_move(self, src_row):
        if self.team == 'w':
            if src_row == 1:
                return [(0, 1), (0, 2)]
            else:
                return [(0, 1)]
        else:
            if src_row == 6:
                return [(0, -1), (0, -2)]
            else:
                return [(0, -1)]

    def threat(self):
        if self.team == 'w':
            return [(1, 1), (-1, 1)]
        else:
            return [(1, -1), (-1, -1)]

    def __str__(self):
        return 'p'


class King(object):
    def __init__(self, team):
        if team in ['w', 'b']:
            self.team = team
        else:
            print('team got to be w or b')
            raise AttributeError
        self.did_king_move = False

    def __str__(self):
        return 'K'

    def optional_move(self, src_row):
        return optional_move_and_threat_king

    def threat(self):
        return optional_move_and_threat_king


class Knight(object):
    def __init__(self, team):
        if team in ['w', 'b']:
            self.team = team
        else:
            print('team got to be w or b')
            raise AttributeError

    def __str__(self):
        return 'n'

    def optional_move(self, src_row):
        return KNIGHT_MOVE_THREAT

    def threat(self):
        return KNIGHT_MOVE_THREAT


class Rook(object):
    def __init__(self, team):
        if team in ['w', 'b']:
            self.team = team
        else:
            print('team got to be w or b')
            raise AttributeError

        self.did_rook_move = False

    def __str__(self):
        return 'r'
        return 'r'

    def optional_move(self, src_row):
        return rook_move_option

    def threat(self):
        return rook_move_option


class Bishop(object):
    def __init__(self, team):
        if team in ['w', 'b']:
            self.team = team
        else:
            print('team got to be w or b')
            raise AttributeError

    def __str__(self):
        return 'b'

    def optional_move(self, src_row):
        return bishop_move_option

    def threat(self):
        return bishop_move_option


class Queen(object):
    def __init__(self, team):
        if team in ['w', 'b']:
            self.team = team
        else:
            print('team got to be w or b')
            raise AttributeError

    def __str__(self):
        return 'Q'

    def optional_move(self, src_row):
        return queen_move_option

    def threat(self):
        return queen_move_option

