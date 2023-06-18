import pygame
from board import Board
import random
import time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("TicTacToe")
img = pygame.image.load("icon.png")
pygame.display.set_icon(img)
screen_width = screen.get_width()
screen_height = screen.get_height()
clock = pygame.time.Clock()
running = True
game_state = "start_menu"
X = "X"
O = "O"
MAX = O
MIN = X
board = Board()
startingPlayer = None
win_state = None
go = False
ai = False

upper_bound = screen_height * 0.1
lower_bound = screen_height - upper_bound
line_length = lower_bound - upper_bound
left_bound = screen_width / 2 - line_length / 2
right_bound = screen_width / 2 + line_length / 2
mid_left_bound = left_bound + line_length / 3
mid_right_bound = right_bound - line_length / 3
mid_upper_bound = upper_bound + line_length / 3
mid_lower_bound = lower_bound - line_length / 3

THICKNESS = 15
X_COLOR = "#DF2935"
O_COLOR = "#3772FF"
LINE_COLOR = "#0F0F0F"
BG_COLOR_1 = "#F7F4F3"

TITLE_FONT = pygame.font.SysFont("monospace", 200)
BUTTON_FONT = pygame.font.SysFont("verdana-bold", 30)

times_played = 0


def start_menu(click):
    # Resets the board for the new game
    board.reset()

    # Renders the actual start menu
    screen.fill(BG_COLOR_1)
    tic = TITLE_FONT.render("TIC", True, LINE_COLOR)
    tac = TITLE_FONT.render("TAC", True, LINE_COLOR)
    toe = TITLE_FONT.render("TOE", True, LINE_COLOR)
    screen.blit(tic, (screen_width / 2 - tic.get_width() / 2, 0))
    screen.blit(tac, (screen_width / 2 - tac.get_width() / 2, 120))
    screen.blit(toe, (screen_width / 2 - toe.get_width() / 2, 240))

    rect1 = pygame.draw.rect(
        screen,
        "grey",
        pygame.Rect(screen_width / 2 - 115, screen_height * 3 / 4 - 65, 230, 50),
    )
    rect2 = pygame.draw.rect(
        screen,
        "grey",
        pygame.Rect(screen_width / 2 - 115, screen_height * 3 / 4, 230, 50),
    )
    rect3 = pygame.draw.rect(
        screen,
        "grey",
        pygame.Rect(screen_width / 2 - 115, screen_height * 3 / 4 + 65, 230, 50),
    )
    if rect1.left < pygame.mouse.get_pos()[0] < rect1.right:
        if rect1.top < pygame.mouse.get_pos()[1] < rect1.bottom:
            rect1 = pygame.draw.rect(
                screen,
                "#5e5e5e",
                pygame.Rect(
                    screen_width / 2 - 115, screen_height * 3 / 4 - 65, 230, 50
                ),
            )
            if click:
                return "play"
        elif rect2.top < pygame.mouse.get_pos()[1] < rect2.bottom:
            rect2 = pygame.draw.rect(
                screen,
                "#5e5e5e",
                pygame.Rect(screen_width / 2 - 115, screen_height * 3 / 4, 230, 50),
            )
            if click:
                return "ai"
        elif rect3.top < pygame.mouse.get_pos()[1] < rect3.bottom:
            rect3 = pygame.draw.rect(
                screen,
                "#5e5e5e",
                pygame.Rect(
                    screen_width / 2 - 115, screen_height * 3 / 4 + 65, 230, 50
                ),
            )
            if click:
                return "quit"
    start_text = BUTTON_FONT.render("START", True, "black")
    ai_text = BUTTON_FONT.render("MINIMAX AI", True, "black")
    quit_text = BUTTON_FONT.render("QUIT", True, "black")

    screen.blit(
        start_text,
        (
            rect1.centerx - start_text.get_width() / 2,
            rect1.centery - start_text.get_height() / 2,
        ),
    )
    screen.blit(
        ai_text,
        (
            rect2.centerx - ai_text.get_width() / 2,
            rect2.centery - ai_text.get_height() / 2,
        ),
    )
    screen.blit(
        quit_text,
        (
            rect3.centerx - quit_text.get_width() / 2,
            rect3.centery - quit_text.get_height() / 2,
        ),
    )

    pygame.display.update()


def play():
    screen.fill(BG_COLOR_1)
    pygame.display.update()
    # Randomly decides who's turn it currently is
    turn = random.randint(0,1)
    global startingPlayer
    startingPlayer = turn
    # None means continue playing, holds value of who won or draw
    winner = None
    runner = True
    while runner:
        display_turn(turn)
        render_lines()

        pygame.display.update()
        # Player Turn
        if turn == 0:
            # If player turn returns a winner, put in winner
            winner = player_turn()
            if not winner == None:
                runner = False
            screen.fill(BG_COLOR_1, (0, 0, screen_width, 70))
            turn = 1
        # Computer Turn
        elif turn == 1:
            # If computer turn returns a winner, put in winner
            winner = computer_turn()
            if not winner == None:
                runner = False
            screen.fill(BG_COLOR_1, (0, 0, screen_width, 70))
            turn = 0

        # If the board is in a draw state break and put a draw in winner
        if board.check_draw():
            time.sleep(2)
            winner = "DRAW"
            runner = False
            break
            
    time.sleep(1)
    return winner


def display_turn(turn):
    turn_display = pygame.font.SysFont("monospace", 65)
    if turn == 0:  # player
        text = turn_display.render("PLAYER TURN", True, X_COLOR)
    elif turn == 1:  # computer
        text = turn_display.render("COMPUTER TURN", True, O_COLOR)

    screen.blit(text, (screen_width / 2 - text.get_width() / 2, 5))
    pygame.display.update()


def player_turn():
    # Checks computer win to quit game loop
    if board.check_win(O):
        return O

    # Prompt user for input
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = get_box()
                if not coords == None:
                    try:
                        board.place(coords[0], coords[1], X)
                    except ValueError:
                        pass
                    else:
                        render_X(coords)
                        pygame.display.update()
                        running = False
    return None


def get_box():
    x, y = pygame.mouse.get_pos()
    if left_bound < x < right_bound:
        if upper_bound < y < lower_bound:
            if x < mid_left_bound:
                if y < mid_upper_bound:
                    return (0, 0)
                elif y > mid_lower_bound:
                    return (2, 0)
                else:
                    return (1, 0)
            elif x > mid_right_bound:
                if y < mid_upper_bound:
                    return (0, 2)
                elif y > mid_lower_bound:
                    return (2, 2)
                else:
                    return (1, 2)
            else:
                if y < mid_upper_bound:
                    return (0, 1)
                elif y > mid_lower_bound:
                    return (2, 1)
                else:
                    return (1, 1)
    return None


def render_X(coords):
    match coords:
        case (0, 0):
            draw_X(left_bound, mid_left_bound, upper_bound, mid_upper_bound)
        case (0, 1):
            draw_X(mid_left_bound, mid_right_bound, upper_bound, mid_upper_bound)
        case (0, 2):
            draw_X(mid_right_bound, right_bound, upper_bound, mid_upper_bound)
        case (1, 0):
            draw_X(left_bound, mid_left_bound, mid_upper_bound, mid_lower_bound)
        case (1, 1):
            draw_X(mid_left_bound, mid_right_bound, mid_upper_bound, mid_lower_bound)
        case (1, 2):
            draw_X(mid_right_bound, right_bound, mid_upper_bound, mid_lower_bound)
        case (2, 0):
            draw_X(left_bound, mid_left_bound, mid_lower_bound, lower_bound)
        case (2, 1):
            draw_X(mid_left_bound, mid_right_bound, mid_lower_bound, lower_bound)
        case (2, 2):
            draw_X(mid_right_bound, right_bound, mid_lower_bound, lower_bound)


def draw_X(x1, x2, y1, y2):
    pygame.draw.line(screen, X_COLOR, (x1 + 30, y1 + 25), (x2 - 30, y2 - 25), THICKNESS)
    pygame.draw.line(screen, X_COLOR, (x1 + 30, y2 - 25), (x2 - 30, y1 + 25), THICKNESS)


def computer_turn():
    # Checks player win to quit game loop
    if board.check_win(X):
        return X
    if ai:
        # Get best computer using minimax input
        play_best_move(board)
    else:
        while True:
            x = random.randint(0,2)
            y = random.randint(0,2)
            if board.state[x][y] == "":
                board.place(x, y, O)
                return None
    

def play_best_move(s):
    moves = []
    values = []
    for action in actions(s):
        moves.append(action)
        values.append(minimax(result(s, action)))
    t = max(values)
    bestMove = values.index(t)

    for i in range(3):
        for j in range(3):
            if not moves[bestMove].state[i][j] == "":
                s.place(i, j, O)
                render_O((i, j))
                pygame.display.update()
    

def minimax(s):
    if isterminal(s):
        return val(s)
    
    if player(s) == MAX:
        num = -10000
        for a in actions(s):
            num = max(num, (minimax(result(s, a))))
        return num
    
    if player(s) == MIN:
        num = 10000
        for a in actions(s):
            num = min(num, (minimax(result(s, a))))
        return num
    
def player(s):
    countX = 0
    countO = 0
    for i in range(3):
        for j in range(3):
            match s.state[i][j]:
                case "X": countX+=1
                case "O": countO+=1

    if startingPlayer == 0:
        if countX == countO:
            return MIN
        elif countX == countO+1:
            return MAX
        else:
            raise ValueError("Incorrect number of Xs or Os")
    else:
        if countX == countO:
            return MAX
        elif countO == countX+1:
            return MIN
        else:
            raise ValueError("Incorrect number of Xs or Os")

        

def isterminal(s):
    return (s.check_win(O) or s.check_win(X) or s.check_draw())

def val(s):
    if s.check_win(O):
        return 1
    elif s.check_win(X):
        return -1
    elif s.check_draw():
        return 0
    else:
        return None
    
def actions(s):
    indicies = []
    for i in range(3):
        for j in range(3):
            if s.state[i][j] == "":
                indicies.append((i,j))
    actions = []
    turn = player(s)
    for r, c in indicies:
        temp = Board()
        temp.place(r, c, turn)
        actions.append(temp)
    return actions

def result(s, a):
    result = Board()
    for i in range(3):
        for j in range(3):
            if (not (s.state[i][j] == "")) and (not (a.state[i][j] == "")):
                raise ValueError("Trying to add two boards that cannot be added.")
            else:
                result.place(i, j, (s.state[i][j] + a.state[i][j]))
    return result

def render_O(coords):
    match coords:
        case (0, 0):
            draw_O(left_bound, mid_left_bound, upper_bound, mid_upper_bound)
        case (0, 1):
            draw_O(mid_left_bound, mid_right_bound, upper_bound, mid_upper_bound)
        case (0, 2):
            draw_O(mid_right_bound, right_bound, upper_bound, mid_upper_bound)
        case (1, 0):
            draw_O(left_bound, mid_left_bound, mid_upper_bound, mid_lower_bound)
        case (1, 1):
            draw_O(mid_left_bound, mid_right_bound, mid_upper_bound, mid_lower_bound)
        case (1, 2):
            draw_O(mid_right_bound, right_bound, mid_upper_bound, mid_lower_bound)
        case (2, 0):
            draw_O(left_bound, mid_left_bound, mid_lower_bound, lower_bound)
        case (2, 1):
            draw_O(mid_left_bound, mid_right_bound, mid_lower_bound, lower_bound)
        case (2, 2):
            draw_O(mid_right_bound, right_bound, mid_lower_bound, lower_bound)


def draw_O(x1, x2, y1, y2):
    pygame.draw.circle(screen, O_COLOR, ((x1 + x2) / 2, (y1 + y2) / 2), 70, THICKNESS)


def render_lines():
    pygame.draw.line(
        screen,
        LINE_COLOR,
        (mid_left_bound, upper_bound),
        (mid_left_bound, lower_bound),
        THICKNESS,
    )
    pygame.draw.line(
        screen,
        LINE_COLOR,
        (mid_right_bound, upper_bound),
        (mid_right_bound, lower_bound),
        THICKNESS,
    )
    pygame.draw.line(
        screen,
        LINE_COLOR,
        (left_bound, mid_upper_bound),
        (right_bound, mid_upper_bound),
        THICKNESS,
    )
    pygame.draw.line(
        screen,
        LINE_COLOR,
        (left_bound, mid_lower_bound),
        (
            right_bound,
            mid_lower_bound,
        ),
        THICKNESS,
    )


def game_over(click):
    screen.fill(BG_COLOR_1)
    font = pygame.font.SysFont("monospace", 200)
    if win_state == "DRAW":
        title = font.render(f"DRAW", True, "black")
        screen.blit(
            title,
            (
                screen_width / 2 - title.get_width() / 2,
                screen_height / 2 - title.get_height() / 2,
            ),
        )
    elif win_state == X:
        you = font.render("YOU", True, "black")
        win = font.render("WIN", True, "black")
        screen.blit(
            you,
            (
                screen_width / 2 - you.get_width() / 2,
                120,
            ),
        )
        screen.blit(
            win,
            (
                screen_width / 2 - win.get_width() / 2,
                240,
            ),
        )
    elif win_state == O:
        you = font.render("YOU", True, "black")
        lose = font.render("LOSE", True, "black")
        screen.blit(
            you,
            (
                screen_width / 2 - you.get_width() / 2,
                120,
            ),
        )
        screen.blit(
            lose,
            (
                screen_width / 2 - lose.get_width() / 2,
                240,
            ),
        )

    rect1 = pygame.draw.rect(
        screen,
        "grey",
        pygame.Rect(screen_width / 2 - 115, screen_height * 3 / 4 - 65, 230, 50),
    )
    rect2 = pygame.draw.rect(
        screen,
        "grey",
        pygame.Rect(screen_width / 2 - 115, screen_height * 3 / 4, 230, 50),
    )
    rect3 = pygame.draw.rect(
        screen,
        "grey",
        pygame.Rect(screen_width / 2 - 115, screen_height * 3 / 4 + 65, 230, 50),
    )
    if rect1.left < pygame.mouse.get_pos()[0] < rect1.right:
        if rect1.top < pygame.mouse.get_pos()[1] < rect1.bottom:
            rect1 = pygame.draw.rect(
                screen,
                "#5e5e5e",
                pygame.Rect(
                    screen_width / 2 - 115, screen_height * 3 / 4 - 65, 230, 50
                ),
            )
            if click:
                return "play"
        elif rect2.top < pygame.mouse.get_pos()[1] < rect2.bottom:
            rect2 = pygame.draw.rect(
                screen,
                "#5e5e5e",
                pygame.Rect(screen_width / 2 - 115, screen_height * 3 / 4, 230, 50),
            )
            if click:
                return "start_menu"
        elif rect3.top < pygame.mouse.get_pos()[1] < rect3.bottom:
            rect3 = pygame.draw.rect(
                screen,
                "#5e5e5e",
                pygame.Rect(
                    screen_width / 2 - 115, screen_height * 3 / 4 + 65, 230, 50
                ),
            )
            if click:
                return "quit"
    start_text = BUTTON_FONT.render("PLAY AGAIN", True, "black")
    ai_text = BUTTON_FONT.render("BACK TO MENU", True, "black")
    quit_text = BUTTON_FONT.render("QUIT", True, "black")

    screen.blit(
        start_text,
        (
            rect1.centerx - start_text.get_width() / 2,
            rect1.centery - start_text.get_height() / 2,
        ),
    )
    screen.blit(
        ai_text,
        (
            rect2.centerx - ai_text.get_width() / 2,
            rect2.centery - ai_text.get_height() / 2,
        ),
    )
    screen.blit(
        quit_text,
        (
            rect3.centerx - quit_text.get_width() / 2,
            rect3.centery - quit_text.get_height() / 2,
        ),
    )
    pygame.display.update()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            go = True
        if event.type == pygame.MOUSEBUTTONUP:
            go = False

    if game_state == "start_menu":
        temp = start_menu(go)
        if temp == "play":
            game_state = "play"
            ai = False
        elif temp == "quit":
            running = False
        elif temp == "ai":
            game_state = "play"
            ai = True
        go = False

    if game_state == "play":
        go = False
        win_state = play()
        game_state = "game_over"

    if game_state == "game_over":
        a = game_over(go)
        times_played += 1
        if a == "play":
            board.reset()
            game_state = "play"
        elif a == "quit":
            running = False
        elif a == "start_menu":
            game_state = "start_menu"
        go = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
