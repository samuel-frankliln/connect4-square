import datetime

import numpy as np
import random
import pygame
import sys
import math

BLUE = (0, 0, 255)
HAZEL_WOOD = (201, 187, 142)
TAN = (230, 219, 172)
BEIGE = (238, 220, 154)
MACAROON = (249, 224, 118)
GRANOLA = (214, 184, 90)
OAT = (223, 201, 138)
EGGNOG = (250, 226, 156)
FAWN = (200, 169, 81)
SUGAR_COOKIE = (243, 234, 175)
SAND = (216, 184, 99)
SEPIA = (227, 183, 120)
LATTE = (231, 194, 125)
OYSTER = (220, 215, 160)
BISCOTTI = (227, 197, 101)
PARMESEAN = (253, 233, 146)
HAZELNUT = (189, 165, 93)
SANDCASTLE = (218, 193, 124)
BUTTERMILK = (253, 239, 178)
SAND_DOLLAR = (237, 232, 186)
SHORTBREAD = (251, 231, 144)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BG = (128,128,128)  # #E3B778

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check for squares of 4 pieces in a row
    for c in range(COLUMN_COUNT - 1):
        for r in range(ROW_COUNT - 1):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r + 1][c] == piece and board[r + 1][
                c + 1] == piece:
                return True


# Evaluate function to check for a 2x2 square
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if len(window) < 5:
        return score

    # Check for square connections
    if window[0] == piece and window[1] == piece and window[3] == piece and window[4] == piece and len(window) >= 8 and window[        2] == EMPTY and window[5] == EMPTY and window[6] == EMPTY and window[7] == EMPTY:
        score += 10
    elif window[1] == piece and window[2] == piece and window[4] == piece and window[5] == piece and len(window) >= 8 and window[        0] == EMPTY and window[3] == EMPTY and window[6] == EMPTY and window[7] == EMPTY:
        score += 10
    elif window[3] == piece and window[4] == piece and window[6] == piece and window[7] == piece and len(window) >= 8 and window[        0] == EMPTY and window[1] == EMPTY and window[2] == EMPTY and window[5] == EMPTY:
        score += 10
    elif window[4] == piece and window[5] == piece and window[7] == piece and window[8] == piece and len(window) >= 9 and window[        0] == EMPTY and window[1] == EMPTY and window[2] == EMPTY and window[3] == EMPTY:
        score += 10

    return score

# Scoring function that prioritizes forming a 2x2 square
def score_position(board, piece):
    score = 0

    # Check horizontal locations for 2x2 squares
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT - 1):
            window = row_array[c:c+2]
            score += evaluate_window(window, piece)

    # Check vertical locations for 2x2 squares
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT - 1):
            window = col_array[r:r+2]
            score += evaluate_window(window, piece)

    # Check diagonals for 2x2 squares
    for r in range(ROW_COUNT - 1):
        for c in range(COLUMN_COUNT - 1):
            window = [board[r+i][c+i] for i in range(2)]
            score += evaluate_window(window, piece)
            window = [board[r+1-i][c+i] for i in range(2)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_player_name(input):
    # Create a text input field for the player's name
    input_rect = pygame.Rect(200, 20, 200, 40)
    player = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return player
                elif event.key == pygame.K_BACKSPACE:
                    player = player[:-1]
                else:
                    player += event.unicode

        # Draw the text input field and player's name
        screen.fill(pygame.Color(BG))
        pygame.draw.rect(screen, pygame.Color('white'), input_rect, 2)
        text_surface = myfont.render(input + player, True, pygame.Color('white'))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.display.update()


def select_player():
    font = pygame.font.Font(None, 30)
    text1 = font.render(player_name, True, (0, 0, 0))
    text2 = font.render("Agent", True, (0, 0, 0))
    global selected_option

    # Initialize radio buttons
    option1 = pygame.Rect(50, 100, 40, 40)
    option2 = pygame.Rect(50, 200, 40, 40)

    # Draw radio buttons and labels
    pygame.draw.rect(screen, (0, 0, 0), option1)
    pygame.draw.rect(screen, (0, 0, 0), option2)
    screen.blit(text1, (100, 95))
    screen.blit(text2, (100, 195))

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return selected_option
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if the mouse is clicked on one of the radio buttons
                if option1.collidepoint(mouse_pos):
                    selected_option = 0
                elif option2.collidepoint(mouse_pos):
                    selected_option = 1

        # Update the radio buttons based on the selected option
        if selected_option == 1:
            pygame.draw.rect(screen, (0, 0, 0), option1)
            pygame.draw.rect(screen, (255, 0, 0), option2)
        elif selected_option == 0:
            pygame.draw.rect(screen, (255, 0, 0), option1)
            pygame.draw.rect(screen, (0, 0, 0), option2)

        pygame.display.update()


def select_board_color():
    colors = [BLUE, BEIGE, MACAROON, HAZEL_WOOD, GRANOLA, OAT, EGGNOG, FAWN, SUGAR_COOKIE, SAND, SEPIA, LATTE, OYSTER,
              BISCOTTI, PARMESEAN, SAND_DOLLAR, SHORTBREAD]
    x, y = 10, 10
    for color in colors:
        button_rect = pygame.Rect(x, y, 30, 30)
        button = {"rect": button_rect, "color": color, "selected": False}
        buttons.append(button)
        x += 40 + 10
        if x >= 800 - 40:
            x = 10
            y += 40 + 10
    global selected_board_color
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a button was clicked
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        for other_button in buttons:
                            other_button["selected"] = False
                        button["selected"] = True
                        selected_board_color = button["color"]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return selected_board_color
        for button in buttons:
            pygame.draw.rect(screen, button["color"], button["rect"])
            if button["selected"]:
                pygame.draw.circle(screen, (128,128,128), (button["rect"].centerx, button["rect"].centery), 8)
            label = myfont.render(str(buttons.index(button)), True, BLACK)
            label_rect = label.get_rect()
            label_rect.center = button["rect"].center
            screen.blit(label, label_rect)
        pygame.display.update()


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, selected_board_color, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BG, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, WHITE, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


game_time = datetime.datetime.now()
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 15)
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
text_color = pygame.Color('white')
selected_option = 0
buttons = []
selected_board_color = ()
select_board_color()
player_name = get_player_name('name: ')
agent_name = 'Agent'
select_player()
minimax_depth = get_player_name('depth: ')
board = create_board()
print_board(board)
game_over = False
turn = selected_option
pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

no_of_moves = 0
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BG, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, BLACK, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BG, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    no_of_moves += 1

                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render(player_name + " wins!! \n Number of moves: " + str(no_of_moves) + " Game Lasted: " + str(datetime.datetime.now() - game_time), 1, BLACK)

                        screen.blit(label, (40, 5))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)

    # # Ask for Player 2 Input
    if turn == AI and not game_over:

        # col = random.randint(0, COLUMN_COUNT-1)
        # col = pick_best_move(board, AI_PIECE)
        col, minimax_score = minimax(board, int(minimax_depth), -math.inf, math.inf, True)

        if is_valid_location(board, col):
            # pygame.time.wait(500)
            no_of_moves += 1
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("Agent wins!! Moves count: " + str(no_of_moves) + " Game Lasted: " + str(datetime.datetime.now() - game_time), 1, BLACK)
                screen.blit(label, (40, 10))
                game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(10000)
