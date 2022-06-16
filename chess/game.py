import pygame
import moves

SIZE = (1000, 800)
SQUARE_WIDTH = int(0.8 * SIZE[0] // 8)
SQUARE_HEIGHT = SIZE[1] // 8
IMAGES = {}
pygame.init()
screen = pygame.display.set_mode(SIZE)
move_feed = []

running = True

board_array = [
    ['Br', 'Bn', 'Bb', 'Bq', 'Bk', 'Bb', 'Bn', 'Br'],
    ['Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp'],
    ['Wr', 'Wn', 'Wb', 'Wq', 'Wk', 'Wb', 'Wn', 'Wr']
]


def load_images():
    pieces = ['Br', 'Bn', 'Bb', 'Bq', 'Bk', 'Bp', 'Wp', 'Wr', 'Wn', 'Wb', 'Wq', 'Wk']
    for piece in pieces:
        img = pygame.transform.scale(pygame.image.load(f'../resources/{piece}.svg'), (SQUARE_WIDTH, SQUARE_HEIGHT))
        IMAGES[piece] = img


def draw_pieces():
    for i in range(8):
        for j in range(8):
            piece = board_array[i][j]
            if piece != '--':
                screen.blit(IMAGES[piece],
                            pygame.Rect(SQUARE_WIDTH * j, SQUARE_HEIGHT * i, SQUARE_WIDTH, SQUARE_HEIGHT))


def draw_board():
    for i in range(8):
        for j in range(8):
            left = SQUARE_WIDTH * j
            top = SQUARE_HEIGHT * i
            square = pygame.Rect(left, top, SQUARE_WIDTH, SQUARE_HEIGHT)
            if i % 2 == 0 and j % 2 != 0:
                pygame.draw.rect(screen, (255, 255, 255), square)
            elif i % 2 != 0 and j % 2 == 0:
                pygame.draw.rect(screen, (255, 255, 255), square)
            else:
                pygame.draw.rect(screen, (255, 125, 0), square)


def handle_move(initial_position, ending_position):
    init_x, init_y = initial_position[0] // SQUARE_WIDTH, initial_position[1] // SQUARE_HEIGHT
    end_x, end_y = ending_position[0] // SQUARE_WIDTH, ending_position[1] // SQUARE_HEIGHT
    piece = board_array[init_y][init_x][1]
    color = board_array[init_y][init_x][0]
    if piece == 'k' and (
            king_and_rook_cords := moves.validate_castles(board_array, (init_y, init_x), (end_y, end_x), move_feed)):

        perform_castles(king_and_rook_cords, (init_y, init_x))
        return color

    elif moves.basic_move_validation(board_array, (init_y, init_x), (end_y, end_x)):
        board_array[end_y][end_x] = board_array[init_y][init_x]
        board_array[init_y][init_x] = '--'
        move_feed.append(((init_y, init_x), (end_y, end_x)))
        return color


def get_piece_color(initial_position):
    init_x, init_y = initial_position[0] // SQUARE_WIDTH, initial_position[1] // SQUARE_HEIGHT
    color = board_array[init_y][init_x][0]
    return color


def perform_castles(king_and_rook_cords, init_king_cords):
    init_y, init_x = init_king_cords
    king_cords, rook_cords, side = king_and_rook_cords
    board_array[king_cords[0]][king_cords[1]] = board_array[init_y][init_x]
    board_array[rook_cords[0]][rook_cords[1]] = board_array[rook_cords[0]][7]
    board_array[init_y][init_x] = '--'
    if side == 'O-O':
        board_array[rook_cords[0]][7] = '--'
    elif side == 'O-O-O':
        board_array[rook_cords[0]][0] = '--'


def highlight_square(cords):
    left = cords[0] // SQUARE_WIDTH * SQUARE_WIDTH
    top = cords[1] // SQUARE_HEIGHT * SQUARE_HEIGHT
    square = pygame.Rect(left, top, SQUARE_WIDTH, SQUARE_HEIGHT)
    pygame.draw.rect(screen, (0, 255, 100), square)


def draw_sidebar():
    square = pygame.Rect(0.8 * SIZE[0], 0, 0.2 * SIZE[0], SIZE[1])
    pygame.draw.rect(screen, (0, 255, 100), square)


count = 0
load_images()
draw_board()
draw_pieces()
draw_sidebar()
pygame.display.update()
last_color_moved = 'B'

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if count == 0:
                initial_pos = event.pos

                if (last_color_moved == 'B' and get_piece_color(initial_pos) == 'W') or (
                        last_color_moved == 'W' and get_piece_color(initial_pos) == 'B'):
                    count += 1
                    draw_board()
                    highlight_square(initial_pos)
                    draw_pieces()
            elif count == 1:
                ending_pos = event.pos
                count = 0
                if color := handle_move(initial_pos, ending_pos):
                    last_color_moved = color
                draw_board()
                draw_pieces()

    pygame.display.update()

pygame.quit()
