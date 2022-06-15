from typing import Tuple


class Pawn:
    @staticmethod
    def has_pawn_moved(init_cords: Tuple[int, int], pawn_color: str) -> bool:
        return (pawn_color == 'B' and init_cords[0] != 1) or (pawn_color == 'W' and init_cords[0] != 6)
