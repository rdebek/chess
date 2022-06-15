from typing import List, Tuple, Union
from pieces.pawn import Pawn
from pieces.king import King


def basic_move_validation(board_state: List[List[str]], init_cords: Tuple[int, int],
                          end_cords: Tuple[int, int]) -> bool:
    piece_color = board_state[init_cords[0]][init_cords[1]][0]
    ending_square_piece_color = board_state[end_cords[0]][end_cords[1]][0]
    if piece_color == ending_square_piece_color:
        return False

    piece_symbol = board_state[init_cords[0]][init_cords[1]][1]

    if piece_symbol == 'n':
        y_movement, x_movement = get_y_and_x_movement(init_cords, end_cords)
        return validate_knight_move(y_movement, x_movement)
    elif piece_symbol == 'b':
        movement = get_y_and_x_movement(init_cords, end_cords)
        return validate_bishop_move(board_state, init_cords, movement)
    elif piece_symbol == 'r':
        movement = get_y_and_x_movement(init_cords, end_cords)
        return validate_rook_move(board_state, init_cords, movement)
    elif piece_symbol == 'q':
        movement = get_y_and_x_movement(init_cords, end_cords)
        return validate_rook_move(board_state, init_cords, movement) or validate_bishop_move(board_state, init_cords,
                                                                                             movement)
    elif piece_symbol == 'p':
        movement = get_y_and_x_movement(init_cords, end_cords)
        return validate_basic_pawn_move(init_cords, movement, piece_color,
                                        ending_square_piece_color) or validate_pawn_capture(
            board_state, init_cords, end_cords)
    elif piece_symbol == 'k':
        movement = get_y_and_x_movement(init_cords, end_cords)
        return validate_basic_king_move(movement)

    return False


def validate_basic_pawn_move(init_cords: Tuple[int, int], movement: Tuple[int, int], pawn_color: str,
                             ending_square_piece_color: str) -> bool:
    y_movement, x_movement = movement

    if x_movement:
        return False

    if ending_square_piece_color != '-':
        return False

    if pawn_color == 'W':
        if y_movement == 2 and Pawn.has_pawn_moved(init_cords, pawn_color):
            return False
        if y_movement > 2 or y_movement < 0:
            return False

    if pawn_color == 'B':
        if y_movement == -2 and Pawn.has_pawn_moved(init_cords, pawn_color):
            return False
        if y_movement < -2 or y_movement > 0:
            return False

    return True


def validate_pawn_capture(board_state: List[List[str]], init_cords: Tuple[int, int],
                          end_cords: Tuple[int, int]) -> bool:
    y_movement, x_movement = get_y_and_x_movement(init_cords, end_cords)
    pawn_color = board_state[init_cords[0]][init_cords[1]][0]
    captured_piece_color = board_state[end_cords[0]][end_cords[1]][0]
    if pawn_color == 'W':
        if y_movement != 1 or x_movement not in [-1, 1]:
            return False
        if captured_piece_color != 'B':
            return False

    elif pawn_color == 'B':
        if y_movement != -1 or x_movement not in [-1, 1]:
            return False
        if captured_piece_color != 'W':
            return False

    return True


def validate_castles(board_state: List[List[str]], init_cords: Tuple[int, int],
                     end_cords: Tuple[int, int], move_history: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> \
        Union[bool, Tuple[Tuple[int, int], Tuple[int, int], str]]:
    movement = get_y_and_x_movement(init_cords, end_cords)
    if validate_king_castle(board_state, init_cords, movement, move_history):
        if movement[1] > 0:
            return (init_cords[0], init_cords[1] - 2), (init_cords[0], init_cords[1] - 1), 'O-O-O'
        elif movement[1] < 0:
            return (init_cords[0], init_cords[1] + 2), (init_cords[0], init_cords[1] + 1), 'O-O'
    return False


def validate_basic_king_move(movement: Tuple[int, int]) -> bool:
    y_movement, x_movement = movement
    return abs(y_movement) <= 1 and abs(x_movement) <= 1


def validate_king_castle(board_state: List[List[str]], init_cords: Tuple[int, int], movement: Tuple[int, int],
                         move_history: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> bool:
    y_movement, x_movement = movement

    if y_movement:
        return False

    if (1 < x_movement <= 3) or (-1 > x_movement >= -4):
        return King.can_castle(board_state, init_cords, x_movement, move_history)

    return False


def validate_rook_move(board_state: List[List[str]], init_cords: Tuple[int, int], movement: Tuple[int, int]) -> bool:
    y_movement, x_movement = movement

    if y_movement and x_movement:
        return False

    move_direction = get_move_direction(y_movement, x_movement)
    init_y, init_x = init_cords

    for i in range(max(abs(y_movement), abs(x_movement)) - 1):
        init_y += move_direction[0]
        init_x += move_direction[1]
        if board_state[init_y][init_x] != '--':
            return False

    return True


def validate_knight_move(y_movement: int, x_movement: int) -> bool:
    if abs(y_movement) == 2 and abs(x_movement) == 1:
        return True
    elif abs(y_movement) == 1 and abs(x_movement) == 2:
        return True
    else:
        return False


def get_y_and_x_movement(init_cords: Tuple[int, int], end_cords: Tuple[int, int]) -> Tuple[int, int]:
    y_movement = init_cords[0] - end_cords[0]
    x_movement = init_cords[1] - end_cords[1]
    return y_movement, x_movement


def get_move_direction(y_movement: int, x_movement: int) -> Tuple[int, int]:
    move_direction = (0, 0)

    if y_movement > 0 and x_movement > 0:
        move_direction = (-1, -1)
    elif y_movement > 0 and x_movement < 0:
        move_direction = (-1, 1)
    elif y_movement < 0 and x_movement < 0:
        move_direction = (1, 1)
    elif y_movement < 0 and x_movement > 0:
        move_direction = (1, -1)
    elif y_movement < 0 and x_movement == 0:
        move_direction = (1, 0)
    elif y_movement > 0 and x_movement == 0:
        move_direction = (-1, 0)
    elif y_movement == 0 and x_movement < 0:
        move_direction = (0, 1)
    elif y_movement == 0 and x_movement > 0:
        move_direction = (0, -1)

    return move_direction


def validate_bishop_move(board_state: List[List[str]], init_cords: Tuple[int, int], movement: Tuple[int, int]) -> bool:
    y_movement, x_movement = movement

    if abs(x_movement) != abs(y_movement):
        return False

    move_direction = get_move_direction(y_movement, x_movement)

    init_y, init_x = init_cords
    for i in range(abs(x_movement) - 1):
        init_y += move_direction[0]
        init_x += move_direction[1]
        if board_state[init_y][init_x] != '--':
            return False
    return True
