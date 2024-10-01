import streamlit as st
import random
import sys

st.title("Create a word search!")


def main():
    """Runs a word search creator in Streamlit."""
    user_words = st.text_input(
        "Please enter the words to place in the word search. Use a space as a separator."
    )
    board_size = st.slider("Select size of word search board.", 10, 20, 15)
    if user_words:
        word_list = user_words.split(" ")
        w = word_search(board_size, word_list)
        w.check_words()
        w.fill_board()
        w.display_board()


class word_search:

    def __init__(self, board_size, words):
        """Initializes a new word_search puzzle.

        Args:
          board_size: The number of rows and columns in the word search board.
          words: A list of words to be placed in the board.

        Initializes the word search puzzle by creating a board of the specified size filled with '.' characters.
        """
        self.words = words
        self.rows = board_size
        self.columns = board_size
        self.board = []
        for r in range(self.rows):
            temp_row = []
            for c in range(self.columns):
                temp_row.append(".")
            self.board.append(temp_row)

    def check_words(self):
        """Checks if the words provided can be placed in the word search puzzle.

        Iterates through each word and performs the following checks:

        1. **Length check:** Ensures the word's length is not greater than the board size.
        2. **Alphabetic check:** Verifies that the word contains only alphabetic characters.
        3. **Space check:** Determines if there's sufficient space on the board to accommodate the word.

        If any of the checks fail, an appropriate error message is displayed. Otherwise, the word is added to the board in a random direction.

        Args:
          None

        Returns:
          None
        """
        for word in self.words:
            if len(word) > self.rows:  # check if word is too long
                st.write(word + " is too long for this word search.")
            elif word.isalpha() is False:  # check if non-alphabetic character in string
                st.write(word + " contains non-alphabetic characters.")
            else:
                direction = random.randint(0, 2)  # # add number of directions as needed
                # check if board has enough space left for word
                blank_rows = any("." * len(word) in "".join(r) for r in self.board)
                blank_cols = self._blank_columns(word)
                if blank_rows is False and blank_cols is False:
                    st.write(word + " does not fit the remaining space.")
                elif blank_rows is False and blank_cols is True:
                    direction = random.randint(0, 1)
                elif blank_rows is True and blank_cols is False:
                    direction = 2
                self._add_words(word, direction)

    def _blank_columns(self, the_word):
        """Checks if there are blank columns in the board that can accommodate the given word.

        Iterates through each column and creates a string representing the column's characters. Then, it checks if the string contains a substring of consecutive dots equal to the word's length.

        Args:
          the_word: The word to check for placement.

        Returns:
          True if there's at least one blank column suitable for the word, otherwise False.
        """
        cols_list = []
        for col in range(self.columns):
            temp_col = ""
            for row in range(self.rows):
                temp_col += self.board[row][col]
            cols_list.append(temp_col)
        return any("." * len(the_word) in c for c in cols_list)

    def _add_words(self, the_word, direction):
        """Adds the specified word to the word search board in the given direction.

        Randomly selects a starting position within the board and attempts to place the word. If the placement is successful, the word is added to the board in uppercase letters. If not, a new starting position is randomly selected and the process is repeated.

        Args:
          the_word: The word to be added to the board.
          direction: The direction in which to place the word (0: down, 1: up, 2: left to right).

        Returns:
          None
        """
        random_row = random.randint(0, self.rows - 1)
        random_column = random.randint(0, self.columns - 1)
        while True:
            if direction == 0 and (random_row + 1) + len(the_word) <= self.rows:  # down
                # check if a letter does not already fill the space
                temp_results = ""
                c = random_row
                for e in the_word:
                    temp_results += self.board[c][random_column]
                    c += 1
                # check if no letter fills the space or the same letter fills the space
                if len(set(temp_results)) == 1 or any(
                    t[0] == t[1] for t in zip(list(temp_results), list(the_word))
                ):
                    c = random_row
                    for l in the_word:
                        self.board[c][random_column] = l.upper()
                        c += 1
                    break
            elif direction == 1 and (random_row + 1) - len(the_word) >= 1:  # up
                # check if a letter does not already fill the space
                temp_results = ""
                c = random_row
                for e in the_word:
                    temp_results += self.board[c][random_column]
                    c -= 1
                # check if no letter fills the space or the same letter fills the space
                if len(set(temp_results)) == 1 or any(
                    t[0] == t[1] for t in zip(list(temp_results), list(the_word))
                ):
                    new_counter = random_row
                    for l in the_word:
                        self.board[new_counter][random_column] = l.upper()
                        new_counter -= 1
                    break
            if (
                direction == 2 and (random_column + 1) + len(the_word) <= self.columns
            ):  # left to right
                # check if a letter does not already fill the space
                temp_results = ""
                c = random_column
                for e in the_word:
                    temp_results += self.board[random_row][c]
                    c += 1
                # check if no letter fills the space or the same letter fills the space
                if len(set(temp_results)) == 1 or any(
                    t[0] == t[1] for t in zip(list(temp_results), list(the_word))
                ):
                    c = random_column
                    for l in the_word:
                        self.board[random_row][c] = l.upper()
                        c += 1
                    break
            random_row = random.randint(0, self.rows - 1)
            random_column = random.randint(0, self.columns - 1)
            continue

    def fill_board(self):
        """Fills the empty cells in the word search board with random uppercase letters.

        Iterates through each cell of the board. If a cell contains a '.', a random uppercase letter is generated and placed in that cell.

        Args:
          None

        Returns:
          None
        """
        for r in enumerate(self.board):
            for c in enumerate(r[1]):
                if self.board[r[0]][c[0]] == ".":
                    rand_int = random.randint(
                        65, 90
                    )  # use unicode to fill board with random letters
                    self.board[r[0]][c[0]] = chr(rand_int)

    def display_board(self):
        """Displays the word search board in a visually appealing format.

        Iterates through each row of the board and prints it as a string with spaces between letters. This creates a clean and readable representation of the board.

        Args:
          None

        Returns:
          None
        """
        for r in self.board:
            st.text(" ".join(r))


if __name__ == "__main__":
    main()  # Call main() if this module is run, but not when imported.
