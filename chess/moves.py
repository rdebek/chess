from typing import List, Tuple


def basic_move_validation(board_state: List[List[str]], init_cords: Tuple[int, int],
                          end_cords: Tuple[int, int]) -> bool:
    if not check_ending_square(board_state, init_cords, end_cords):
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
    elif piece_symbol == 'k':
        movement = get_y_and_x_movement(init_cords, end_cords)
        return basic_king_move_validation(movement)

    return False


def basic_king_move_validation(movement: Tuple[int, int]):
    y_movement, x_movement = movement
    return y_movement <= 1 and x_movement <= 1


def validate_rook_move(board_state: List[List[str]], init_cords: Tuple[int, int], movement: Tuple[int, int]):
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


def check_ending_square(board_state: List[List[str]], init_cords: Tuple[int, int], end_cords: Tuple[int, int]) -> bool:
    moving_piece_color = board_state[init_cords[0]][init_cords[1]][0]
    ending_square_piece_color = board_state[end_cords[0]][end_cords[1]][0]

    return moving_piece_color != ending_square_piece_color
