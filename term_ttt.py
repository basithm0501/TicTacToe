from board import Board
import random
import sys
import time

X = "X"
O = "O"
MAX = O
MIN = X
board = Board()
startingPlayer = random.randint(0,1)

def main():
    print("Welcome to TicTacToe!")

    # a = Board()
    # a.set_state([
    #     ["", "", "X"],
    #     ["O", "X", "X"],
    #     ["O", "X", "O"]
    # ])
    # play_best_move(a)

    board.reset()
    game()

def game():
    # Randomly decides who's turn it currently is
    turn = startingPlayer
    # None means continue playing, holds value of who won or draw
    winner = None
    while winner == None:
        print(board)

        # If the board is in a draw state break and put a draw in winner
        if board.check_draw():
            winner = "DRAW"
            break

        # Player Turn
        if turn == 0:
            # If player turn returns a winner, put in winner
            winner = player_turn()
            turn = 1
        # Computer Turn
        elif turn == 1:
            # If computer turn returns a winner, put in winner
            winner = computer_turn()
            turn = 0
    
    if winner == "DRAW":
        print("DRAW GAME")
    elif winner == X:
        print("You win!")
    elif winner == O:
        print("You lost!")

def player_turn():
    # Checks computer win to quit game loop
    if board.check_win(O):
        return(O)
    
    print("-- PLAYER TURN --")

    # Prompt user for input
    while True:
        try: 
            row = int(input("Enter row: "))
            col = int(input("Enter column: "))
            board.place(row-1, col-1, X)
        except ValueError:
            print("Invalid Input")
        else:
            break
    return None


def computer_turn():
    # Checks player win to quit game loop
    if board.check_win(X):
        return(X)
    
    print("-- COMPUTER TURN --")
    time.sleep(random.random())

    # Get random computer input
    play_best_move(board)
    return None

def play_best_move(s):
    # while True:
    #     x = random.randint(0, 2)
    #     y = random.randint(0, 2)
    #     if board.state[x][y] == "":
    #         board.place(x, y, O)
    #         break

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

if __name__ == "__main__":
    main()