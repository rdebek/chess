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
                if move[0] == (7, 4) or (move[0] == (7, 7) and x_movement < 0) or (move[0] == (7, 0) and x_movement > 0):
                    return False
        elif king_color == 'B':
            for move in move_history:
                if move[0] == (0, 4) or (move[0] == (0, 7) and x_movement < 0) or (move[0] == (0, 0) and x_movement > 0):
                    return False
        return True
