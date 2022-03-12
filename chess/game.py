import pygame

SIZE = (800, 800)
SQUARE_WIDTH = SIZE[0] / 8
SQUARE_HEIGHT = SIZE[1] / 8
IMAGES = {}
pygame.init()
screen = pygame.display.set_mode(SIZE)

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
                screen.blit(IMAGES[piece], pygame.Rect(SQUARE_WIDTH * j, SQUARE_HEIGHT * i, SQUARE_WIDTH, SQUARE_HEIGHT))


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


def handle_move(initial_pos, ending_pos):
    init_x, init_y = initial_pos[0]//100, initial_pos[1]//100
    end_x, end_y = ending_pos[0]//100, ending_pos[1]//100
    board_array[end_y][end_x] = board_array[init_y][init_x]
    board_array[init_y][init_x] = '--'


count = 0
load_images()
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if count == 0:
                initial_pos = event.pos
                count += 1
            elif count == 1:
                ending_pos = event.pos
                count = 0
                handle_move(initial_pos, ending_pos)

    draw_board()
    draw_pieces()
    pygame.display.update()

pygame.quit()
