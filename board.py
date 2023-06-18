# Class that holds the Tic Tac Toe board
class Board:
    def __init__(self):
        # self.state holds a list of 3 lists that represents the board, starts with ""
        self.state = [["", "", ""], 
                      ["", "", ""], 
                      ["", "", ""]]

    # Returns board like format to be printed
    def __str__(self):
        return f"{self.state[0]}\n{self.state[1]}\n{self.state[2]}"

    # Places the specified val in the specified position of the board, only if empty
    def place(self, row, col, val):
        if self.state[row][col] == "":
            self.state[row][col] = val
        else:
            raise ValueError
        return

    def set_state(self, s):
        for i in range(3):
            for j in range(3):
                temp = s[i][j]
                self.state[i][j] = temp

    # Checks to see if the board is in a win state for val
    def check_win(self, val):
        for i in range(3):
            # Checks row wins
            if val == self.state[i][0] == self.state[i][1] == self.state[i][2]:
                return True
            # Checks column wins
            if val == self.state[0][i] == self.state[1][i] == self.state[2][i]:
                return True
        # Checks diagonal win (Case 1)
        if val == self.state[0][0] == self.state[1][1] == self.state[2][2]:
            return True
        # Checks diagonal win (Case 2)
        if val == self.state[2][0] == self.state[1][1] == self.state[0][2]:
            return True

        return False

    # Checks to see if the board is in a draw state
    def check_draw(self):
        for i in range(3):
            for j in range(3):
                # Checks for any empty space, if found then not a draw
                if self.state[i][j] == "":
                    return False
        # If the board is full return the opposite of its a win or not
        return not (self.check_win("X") or self.check_win("O"))
    
    # Resets the board
    def reset(self):
        self.state = [["", "", ""], 
                      ["", "", ""], 
                      ["", "", ""]]