from typing import List, Tuple


def basic_move_validation(board_state: List[List[str]], init_cords: Tuple[int], end_cords: Tuple[int]) -> bool:
    return True


def validate_knight_move(init_cords: Tuple[int], end_cords: Tuple[int]) -> bool:
    if abs(init_cords[0] - end_cords[0]) == 2 and abs(init_cords[1] - end_cords[1]) == 1:
        return True
    elif abs(init_cords[0] - end_cords[0]) == 1 and abs(init_cords[1] - end_cords[1]) == 2:
        return True
    else:
        return False


def get_y_and_x_movement(init_cords: Tuple[int], end_cords: Tuple[int]) -> Tuple[int, int]:
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

    return move_direction


def validate_bishop_move(board_state: List[List[str]], init_cords: Tuple[int], movement: Tuple[int, int]) -> bool:
    y_movement, x_movement = movement

    if abs(x_movement) != abs(y_movement):
        return False

    move_direction = get_move_direction(y_movement, x_movement)

    for i in range(abs(x_movement) - 1):
        if board_state[init_cords[0] + move_direction[0]][init_cords[1] + move_direction[1]] != '--':
            return False
    return True


def check_ending_square(board_state: List[List[str]], init_cords: Tuple[int], end_cords: Tuple[int]) -> bool:
    moving_piece_color = board_state[init_cords[0]][init_cords[1]][0]
    ending_square_piece_color = board_state[end_cords[0]][end_cords[1]][0]

    return moving_piece_color != ending_square_piece_color
