from Tools_chess import King,Queen, Bishop, Rook, Knight

DICT_PLACE_TO_NUM = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7
}


def get_move():
    """
    get user move
    :return: 4 index: src col and row, dst col and row
    """
    while True:
        src = input('enter src')
        dst = input('enter dst')
        try:
            return DICT_PLACE_TO_NUM[src[0]], int(src[1])-1, DICT_PLACE_TO_NUM[dst[0]], int(dst[1])-1
        except IndexError:
            print('unknown src or dst')
        except KeyError:
            print('unknown src or dst')


def get_player(counter):
    """
    :param: counter: int
    finds out if it is white or black turn
    :return: str
    """
    if counter % 2 == 0:
        return 'w'
    else:
        return 'b'


def get_threated_place(col, row, tool):
    """
    :param col: int 0-7
    :param row: int 0-7
    :param tool: tool object
    :return: list of threated place by the tool
    """
    [(col + faze[0], row + faze[1]) for faze in tool.threat()]
    threated_places = []
    for faze in tool.threat():
        new_col = (col + faze[0])
        new_row = (row + faze[1])
        if new_col >= 0 and new_row >= 0:
            threated_places.append((new_col, new_row))
    return threated_places


def is_castlite(tool, src_col, dst_col):
    if type(tool) is King and abs(src_col-dst_col) == 2:
        return True
    return False


def get_rooks_original_positions(team):
    if team == 'w':
        return [(0, 0), (7, 0)]
    elif team == 'b':
        return [(0, 7), (7, 7)]
    else:
        raise ValueError


def new_rng(start, end):
    if end < start:
        return [-num for num in range(-start + 1, -end)]
    return list(range(start + 1, end))


def get_squeres_in_way(src_col, src_row, dst_col, dst_row):
    col_indexes = new_rng(src_col, dst_col)
    row_indexes = new_rng(src_row, dst_row)

    if len(col_indexes) == 0:
        for one_index in row_indexes:
            col_indexes.append(src_col)
    elif len(row_indexes) == 0:
        for one_index in col_indexes:
            row_indexes.append(src_row)
    return list(zip(col_indexes, row_indexes))


def get_new_tool(team):
    while True:
        new_tool = input('choose which tool you want')
        if new_tool == 'Q':
            return Queen(team)
        if new_tool == 'n':
            return Knight(team)
        if new_tool == 'r':
            new_tool = Rook(team)
            new_tool.did_rook_move = True
            return new_tool
        if new_tool == 'b':
            return Bishop(team)
        else:
            print('not legal new tool')