class Board:
    """
    Class that represents the Tic Tac Toe board.
    """

    def __init__(self):
        """
        Initializes the board with an empty state.
        """

        self.state = [["", "", ""], 
                      ["", "", ""], 
                      ["", "", ""]]

    def __str__(self):
        """
        Returns a string representation of the board.

        Returns:
            str: String representation of the board.
        """

        return f"{self.state[0]}\n{self.state[1]}\n{self.state[2]}"

    def place(self, row, col, val):
        """
        Places the specified value in the specified position of the board, if the position is empty.

        Args:
            row (int): The row index of the position to place the value.
            col (int): The column index of the position to place the value.
            val (str): The value to be placed in the position.

        Raises:
            ValueError: If the specified position is already occupied.

        Returns:
            None
        """

        if self.state[row][col] == "":
            self.state[row][col] = val
        else:
            raise ValueError("Specified position is already occupied.")
    
    def set_state(self, s):
        """
        Sets the state of the board using the provided 2D list.

        Args:
            s (list): A 2D list representing the new state of the board.
        
        Returns:
            None
        """

        for i in range(3):
            for j in range(3):
                temp = s[i][j]
                self.state[i][j] = temp

    def check_win(self, val):
        """
        Checks if the board is in a win state for the specified value.

        Args:
            val (str): The value to check for a win state.

        Returns:
            bool: True if the board is in a win state for the specified value, False otherwise.
        """

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

    def check_draw(self):
        """
        Checks if the board is in a draw state.

        Returns:
            bool: True if the board is in a draw state, False otherwise.
        """

        for i in range(3):
            for j in range(3):
                # Checks for any empty space, if found then not a draw
                if self.state[i][j] == "":
                    return False
        # If the board is full return the opposite of whether it is a win or not
        return not (self.check_win("X") or self.check_win("O"))
    
    def reset(self):
        """
        Resets the board by setting all positions to empty.

        Returns:
            None
        """

        self.state = [["", "", ""], 
                      ["", "", ""], 
                      ["", "", ""]]
