import pygame
from board import Board
import random
import time

# pygame setup
pygame.init()

# Create the game window
screen = pygame.display.set_mode((700, 700))

# Set the window title and icon
pygame.display.set_caption("TicTacToe")
img = pygame.image.load("icon.png")
pygame.display.set_icon(img)

# Get the dimensions of the game window
screen_width = screen.get_width()
screen_height = screen.get_height()

# Initialize the game clock
clock = pygame.time.Clock()

# Set the initial state of the game
running = True
game_state = "start_menu"

# Define the markers for the players
X = "X"
O = "O"

# Define the players for the minimax algorithm
MAX = O
MIN = X

# Create an instance of the Board class to represent the game board
board = Board()

# Initialize variables for player selection and win state
startingPlayer = None
win_state = None

# Flag to indicate if it's the AI's turn to play
go = False

# Flag to indicate if AI mode is enabled
ai = False

# Define the boundaries and dimensions of the Tic Tac Toe board on the screen
upper_bound = screen_height * 0.1
lower_bound = screen_height - upper_bound
line_length = lower_bound - upper_bound
left_bound = screen_width / 2 - line_length / 2
right_bound = screen_width / 2 + line_length / 2
mid_left_bound = left_bound + line_length / 3
mid_right_bound = right_bound - line_length / 3
mid_upper_bound = upper_bound + line_length / 3
mid_lower_bound = lower_bound - line_length / 3

# Define constants necessary for the rendering process
THICKNESS = 15
X_COLOR = "#DF2935"
O_COLOR = "#3772FF"
LINE_COLOR = "#0F0F0F"
BG_COLOR_1 = "#F7F4F3"
TITLE_FONT = pygame.font.SysFont("monospace", 200)
BUTTON_FONT = pygame.font.SysFont("verdana-bold", 30)

def start_menu(click):
    """
    Renders the start menu of the Tic Tac Toe game and handles button clicks.

    Args:
        click (bool): Indicates if a mouse click event occurred.

    Returns:
        str: Represents the selected option: "play" (start a new game),
            "ai" (play against the AI), or "quit" (quit the game).
    """

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

    # Draw the buttons for game options
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

    # Check for button clicks
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

    # Render button texts
    start_text = BUTTON_FONT.render("START", True, "black")
    ai_text = BUTTON_FONT.render("MINIMAX AI", True, "black")
    quit_text = BUTTON_FONT.render("QUIT", True, "black")

    # Blit button texts onto the screen
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
    """
    Executes the main gameplay loop for the Tic Tac Toe game, alternating between player and computer turns.

    Returns:
        str: Represents the outcome of the game: "X" (player X wins), "O" (player O wins),
            "DRAW" (the game ends in a draw).
    """

    # Fill the screen with the background color
    screen.fill(BG_COLOR_1)
    pygame.display.update()

    # Randomly decide whose turn it currently is
    turn = random.randint(0, 1)
    global startingPlayer
    startingPlayer = turn

    # None means continue playing, holds value of who won or draw
    winner = None
    runner = True
    while runner:
        # Render the current turn
        render_turn(turn)
        render_lines()
        pygame.display.update()

        # Player's Turn
        if turn == 0:
            # If player's turn returns a winner, assign it to the 'winner' variable
            winner = player_turn()
            if not winner == None:
                runner = False
            screen.fill(BG_COLOR_1, (0, 0, screen_width, 70))
            turn = 1
        # Computer's Turn
        elif turn == 1:
            # If computer's turn returns a winner, assign it to the 'winner' variable
            winner = computer_turn()
            if not winner == None:
                runner = False
            screen.fill(BG_COLOR_1, (0, 0, screen_width, 70))
            turn = 0

        # If the board is in a draw state, break the loop and assign "DRAW" to 'winner'
        if board.check_draw():
            time.sleep(2)
            winner = "DRAW"
            runner = False
            break

    time.sleep(1)
    return winner



def render_turn(turn):
    """
    Renders and displays the text indicating whose turn it is.

    Args:
        turn (int): The current turn. 0 represents the player's turn, 1 represents the computer's turn.
    """

    # Create a font for displaying the turn
    turn_display = pygame.font.SysFont("monospace", 65)

    if turn == 0:  # Player's turn
        # Render the text for player's turn with the X color
        text = turn_display.render("PLAYER TURN", True, X_COLOR)
    elif turn == 1:  # Computer's turn
        # Render the text for computer's turn with the O color
        text = turn_display.render("COMPUTER TURN", True, O_COLOR)

    # Display the turn text at the center of the screen
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, 5))
    pygame.display.update()


def player_turn():
    """
    Executes the player's turn in the game.

    Returns:
        str or None: Represents the outcome of the game if a winner is determined,
            or None if the game is still ongoing.
    """

    # Checks if the computer has won to quit the game loop
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
                        # Place the player's symbol (X) on the board
                        board.place(coords[0], coords[1], X)
                    except ValueError:
                        # Ignore if the selected box is already occupied
                        pass
                    else:
                        # Render the player's symbol (X) on the screen
                        render_X(coords)
                        pygame.display.update()
                        running = False
    return None




def get_box():
    """
    Returns the coordinates of the box on the game board corresponding to the current mouse position.
    The game board is divided into 9 equal-sized boxes.

    Returns:
        tuple: The coordinates of the selected box in the format (row, column). Returns None if no box is selected.
    """

    # Get the current mouse position
    x, y = pygame.mouse.get_pos()

    # Check if the mouse position is within the game board bounds
    if left_bound < x < right_bound:
        if upper_bound < y < lower_bound:
            # Determine the row and column based on the mouse position
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
    
    # Return None if no box is selected
    return None



def render_X(coords):
    """
    Renders the X symbol on the game board based on the given coordinates.

    Args:
        coords (tuple): The coordinates of the box where the X symbol should be rendered.
                        Should be in the format (row, column).
    """

    # Use pattern matching to determine the specific coordinates and draw the X symbol accordingly
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
    """
    Draws the X symbol on the game board between the specified coordinates.

    Args:
        x1 (int): The x-coordinate of the starting point of the X symbol.
        x2 (int): The x-coordinate of the ending point of the X symbol.
        y1 (int): The y-coordinate of the starting point of the X symbol.
        y2 (int): The y-coordinate of the ending point of the X symbol.
    """

    # Draw the two diagonal lines to form the X symbol
    pygame.draw.line(screen, X_COLOR, (x1 + 30, y1 + 25), (x2 - 30, y2 - 25), THICKNESS)
    pygame.draw.line(screen, X_COLOR, (x1 + 30, y2 - 25), (x2 - 30, y1 + 25), THICKNESS)



def computer_turn():
    """
    Performs the computer's turn in the game.

    Returns:
        str or None: The symbol of the winner if there is a winner, None otherwise.
    """

    # Checks if the player has won to quit the game loop
    if board.check_win(X):
        return X

    # AI-controlled computer turn
    if ai:
        # Checks if the board is empty
        empty = True
        for i in range(3):
            for j in range(3):
                if not board.state[i][j] == "":
                    empty = False
                    break
        if not empty:
            # Play the best move using the minimax algorithm
            play_best_move(board)
        else:
            # If the board is empty, make the first move in the top-left corner
            time.sleep(1)
            board.place(0, 0, O)
            render_O((0, 0))
        return None
    else:
        # Random computer turn
        while True:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            if board.state[x][y] == "":
                board.place(x, y, O)
                render_O((x, y))
                return None

    

def play_best_move(s):
    """
    Plays the best move for the computer using the minimax algorithm.

    Args:
        s (Board): The current state of the game.

    Returns:
        None
    """

    moves = []
    values = []

    # Calculate the minimax value for each possible action
    for action in actions(s):
        moves.append(action)
        values.append(minimax(result(s, action)))

    # Find the maximum minimax value
    t = max(values)
    bestMove = values.index(t)

    # Place the computer's symbol in the position corresponding to the best move
    for i in range(3):
        for j in range(3):
            if not moves[bestMove].state[i][j] == "":
                s.place(i, j, O)
                render_O((i, j))
                pygame.display.update()

    

def minimax(s):
    """
    Performs the minimax algorithm to determine the best possible score for the current state.

    Args:
        s (Board): The current state of the game.

    Returns:
        int: The score associated with the current state.
    """

    if isterminal(s):
        return val(s)

    if player(s) == MAX:
        num = -10000
        for a in actions(s):
            num = max(num, minimax(result(s, a)))
        return num

    if player(s) == MIN:
        num = 10000
        for a in actions(s):
            num = min(num, minimax(result(s, a)))
        return num


def player(s):
    """
    Determines the player (MAX or MIN) based on the number of Xs and Os on the board.

    Args:
        s (Board): The current state of the game.

    Returns:
        int: The player constant (MAX or MIN).
    
    Raises:
        ValueError: If the number of Xs and Os does not match the expected counts.
    """

    countX = 0
    countO = 0

    # Count the number of Xs and Os on the board
    for i in range(3):
        for j in range(3):
            match s.state[i][j]:
                case "X": countX += 1
                case "O": countO += 1

    # Determine the player based on the starting player and the counts
    if startingPlayer == 0:
        if countX == countO:
            return MIN
        elif countX == countO + 1:
            return MAX
        else:
            raise ValueError("Incorrect number of Xs or Os")
    elif startingPlayer == 1:
        if countX == countO:
            return MAX
        elif countO == countX + 1:
            return MIN
        else:
            raise ValueError("Incorrect number of Xs or Os")
    else:
        raise ValueError("Trying to check whose turn with no startingPlayer")


def isterminal(s):
    """
    Checks if the current state is a terminal state (win or draw).

    Args:
        s (Board): The current state of the game.

    Returns:
        bool: True if the state is terminal, False otherwise.
    """

    return s.check_win(O) or s.check_win(X) or s.check_draw()


def val(s):
    """
    Determines the value associated with the current state.

    Args:
        s (Board): The current state of the game.

    Returns:
        int or None: The value of the state. 1 for win (O), -1 for win (X), 0 for draw, None otherwise.
    """

    if s.check_win(O):
        return 1
    elif s.check_win(X):
        return -1
    elif s.check_draw():
        return 0
    else:
        return None


def actions(s):
    """
    Generates all possible valid actions for the current state.

    Args:
        s (Board): The current state of the game.

    Returns:
        list[Board]: A list of possible valid actions (successor states).
    """

    indices = []
    for i in range(3):
        for j in range(3):
            if s.state[i][j] == "":
                indices.append((i, j))

    actions = []
    turn = player(s)
    for r, c in indices:
        temp = Board()
        temp.place(r, c, turn)
        actions.append(temp)

    return actions


def result(s, a):
    """
    Computes the result of applying an action to a state.

    Args:
        s (Board): The current state of the game.
        a (Board): The action (successor state) to apply.

    Returns:
        Board: The resulting state after applying the action.
    
    Raises:
        ValueError: If two boards cannot be added together.
    """

    result = Board()
    for i in range(3):
        for j in range(3):
            if (not (s.state[i][j] == "")) and (not (a.state[i][j] == "")):
                raise ValueError("Trying to add two boards that cannot be added.")
            else:
                result.place(i, j, (s.state[i][j] + a.state[i][j]))
    return result


def render_O(coords):
    """
    Renders the O symbol on the screen based on the provided coordinates.

    Args:
        coords (tuple): The coordinates (row, column) where the O symbol should be rendered.
    """

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
    """
    Draws the O symbol on the screen based on the provided coordinates.

    Args:
        x1 (int): The left x-coordinate of the O symbol.
        x2 (int): The right x-coordinate of the O symbol.
        y1 (int): The upper y-coordinate of the O symbol.
        y2 (int): The lower y-coordinate of the O symbol.
    """

    pygame.draw.circle(screen, O_COLOR, ((x1 + x2) // 2, (y1 + y2) // 2), 70, THICKNESS)



def render_lines():
    """
    Renders the lines that form the Tic-Tac-Toe grid on the screen.
    """

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
        (right_bound, mid_lower_bound),
        THICKNESS,
    )



def game_over(click):
    """
    Displays the game over screen with the appropriate messages based on the win state.
    Allows the player to choose to play again, go back to the start menu, or quit the game.
    
    Args:
        click (bool): Indicates whether a click event occurred.

    Returns:
        str: The chosen action based on the player's click: "play" for play again, "start_menu" for start menu, or "quit" for quit.
    """

    screen.fill(BG_COLOR_1)
    font = pygame.font.SysFont("monospace", 200)
    
    if win_state == "DRAW":
        # Display draw message
        title = font.render(f"DRAW", True, "black")
        screen.blit(
            title,
            (
                screen_width / 2 - title.get_width() / 2,
                screen_height / 2 - title.get_height() / 2,
            ),
        )
    elif win_state == X:
        # Display win message for player
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
        # Display lose message for player
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

    # Create clickable rectangles for buttons
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

    # Handle button interactions
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

    # Render button text on the screen
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
    # Poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            go = True
        if event.type == pygame.MOUSEBUTTONUP:
            go = False

    if game_state == "start_menu":
        # Handle start menu state
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
        # Handle play state
        go = False
        win_state = play()
        game_state = "game_over"

    if game_state == "game_over":
        # Handle game over state
        a = game_over(go)
        if a == "play":
            board.reset()
            game_state = "play"
        elif a == "quit":
            running = False
        elif a == "start_menu":
            game_state = "start_menu"
        go = False

    # Flip() the display to put your work on the screen
    pygame.display.flip()

    clock.tick(60)  # Limit FPS to 60

pygame.quit()
