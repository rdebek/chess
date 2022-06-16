from typing import List, Tuple


class King:
    @staticmethod
    def can_castle(board_state: List[List[str]], init_cords: Tuple[int, int], x_movement: int,
                   move_history: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> bool:

        king_color = board_state[init_cords[0]][init_cords[1]][0]

        if not King.check_history(move_history, king_color, x_movement):
            return False

        if king_color == 'W':
            if init_cords != (7, 4):
                return False
            elif x_movement < 0:
                for i in range(5, 7):
                    if board_state[7][i][0] != '-':
                        return False
            elif x_movement > 0:
                for i in range(1, 4):
                    if board_state[7][i][0] != '-':
                        return False
        elif king_color == 'B':
            if init_cords != (0, 4):
                return False
            elif x_movement < 0:
                for i in range(5, 7):
                    if board_state[0][i][0] != '-':
                        return False
            elif x_movement > 0:
                for i in range(1, 4):
                    if board_state[0][i][0] != '-':
                        return False
        return True

    @staticmethod
    def check_history(move_history: List[Tuple[Tuple[int, int], Tuple[int, int]]], king_color: str,
                      x_movement: int) -> bool:
        if king_color == 'W':
            for move in move_history:
                if move[0] == (7, 4) or (move[0] == (7, 7) and x_movement < 0) or (
                        move[0] == (7, 0) and x_movement > 0):
                    return False
        elif king_color == 'B':
            for move in move_history:
                if move[0] == (0, 4) or (move[0] == (0, 7) and x_movement < 0) or (
                        move[0] == (0, 0) and x_movement > 0):
                    return False
        return True

    @staticmethod
    def is_in_check(board_state: List[List[str]], king_color: str) -> bool:
        king_position = ''
        for i, row in enumerate(board_state):
            for j, column in enumerate(row):
                if column == f'{king_color}k':
                    king_position = (i, j)
                    break
        return not (King.verify_pawn_checks(board_state, king_position) and King.verify_diagonal_checks(board_state, king_position) and King.verify_row_checks(board_state, king_position))

    @staticmethod
    def verify_pawn_checks(board_state: List[List[str]], king_position: Tuple[int, int]) -> bool:
        king_y, king_x = king_position
        king_color = board_state[king_y][king_x][0]
        if king_color == 'W':
            if board_state[king_y - 1][king_x - 1] == 'Bp' or board_state[king_y - 1][king_x + 1] == 'Bp':
                return False

        elif king_color == 'B':
            if board_state[king_y + 1][king_x - 1] == 'Wp' or board_state[king_y + 1][king_x + 1] == 'Wp':
                return False
        return True

    @staticmethod
    def verify_diagonal_checks(board_state: List[List[str]], king_position: Tuple[int, int]) -> bool:
        king_y, king_x = king_position
        king_color = board_state[king_y][king_x][0]
        diagonal_directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        for direction in diagonal_directions:
            if not King.check_row_or_diagonal(board_state, king_position, direction, king_color, 'diagonal'):
                return False
        return True

    @staticmethod
    def verify_row_checks(board_state: List[List[str]], king_position: Tuple[int, int]) -> bool:
        king_y, king_x = king_position
        king_color = board_state[king_y][king_x][0]
        row_directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for direction in row_directions:
            if not King.check_row_or_diagonal(board_state, king_position, direction, king_color, 'row'):
                return False
        return True

    @staticmethod
    def check_row_or_diagonal(board_state: List[List[str]], start_square: Tuple[int, int], direction: Tuple[int, int],
                  king_color: str, check_type: str) -> bool:
        piece_to_check = 'r' if check_type == 'row' else 'b'
        current_y, current_x = start_square
        dir_y, dir_x = direction
        enemy_color = 'W' if king_color == 'B' else 'B'
        current_y += dir_y
        current_x += dir_x
        while 7 >= current_y >= 0 and 7 >= current_x >= 0:
            if board_state[current_y][current_x] == f'{enemy_color}{piece_to_check}' or board_state[current_y][current_x] == f'{enemy_color}q':
                return False
            elif board_state[current_y][current_x][0] == king_color:
                return True
            current_y += dir_y
            current_x += dir_x
        return True
