import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines_cells = set()
        if len(self.cells) == self.count:
            for cell in self.cells:
                mines_cells.add(cell)
        return mines_cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safes_cells = set()
        if self.count == 0:
            for cell in self.cells:
                safes_cells.add(cell)
        return safes_cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        The mark_mine function should first check to see if cell is one of the cells included in the sentence.
        If cell is in the sentence, the function should update the sentence so that cell is no longer in the sentence, 
        but still represents a logically correct sentence given that cell is known to be a mine.
        If cell is not in the sentence, then no action is necessary.
        """
        if ((cell in self.cells) and (len(self.cells) > 1)):
            self.cells.discard(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        The mark_safe function should first check to see if cell is one of the cells included in the sentence.
        If cell is in the sentence, the function should update the sentence so that cell is no longer in the sentence, 
        but still represents a logically correct sentence given that cell is known to be safe.
        If cell is not in the sentence, then no action is necessary.
        """
        if ((cell in self.cells) and (len(self.cells) > 1)):
            self.cells.discard(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 2) mark the cell as safe
        self.mark_safe(cell)
        # 3) add a new sentence to the AI's knowledge base value of `cell` and `count`
        # The function should add a new sentence to the AI’s knowledge base,
        # based on the value of cell and count, to indicate that count of the cell’s neighbors are mines.
        # Be sure to only include cells whose state is still undetermined in the sentence.

        #   #Loop over all cells within one row and column
        ai_sentence = Sentence(cells=set(), count=int)
        ai_sentence.count = count
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # add cell to knowledge sentence if cell in bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) in self.safes:
                        continue
                    if (i, j) in self.mines:
                        ai_sentence.count -= 1
                    else:
                        ai_sentence.cells.add((i, j))

        #   #add sentence = count to Knowledge
        if len(ai_sentence.cells) > 0:
            self.knowledge.append(ai_sentence)
        # 4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        # If, based on any of the sentences in self.knowledge,
        # new cells can be marked as safe or as mines, then the function should do so.
        # ###add a loop until knowledge is the same
        
        for sentence in self.knowledge:
            new_safes = sentence.known_safes()
            if len(new_safes) == 0:
                if sentence.known_mines():
                    for mine_cell in sentence.known_mines():
                        self.mark_mine(mine_cell)
            else:
                for safe_cell in new_safes:
                    if safe_cell not in self.safes:
                        self.mark_safe(safe_cell)
            
        # 5) add any new sentences to the AI's knowledge base
        # if they can be inferred from existing knowledge
        # If, based on any of the sentences in self.knowledge, new sentences can be inferred
        # (using the subset method described in the Background),
        # then those sentences should be added to the knowledge base as well.
        # Note that any time that you make any change to your AI’s knowledge,
        # it may be possible to draw new inferences that weren’t possible before.
        # Be sure that those new inferences are added to the knowledge base if it is possible to do so.
        # ###while loop to refresh knowledge after 
        
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence2 == sentence1:
                    continue
                else:
                    if sentence1.cells.issubset(sentence2.cells):
                        sentence2.cells = (sentence2.cells) - (sentence1.cells)
                        sentence2.count -= sentence1.count
                        if sentence2.known_safes():
                            for safe_cell in sentence2.known_safes():
                                self.mark_safe(safe_cell)
                        if sentence2.known_mines():
                            for mine_cell in sentence2.known_mines():
                                self.mark_mine(mine_cell)
 
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) > 0:
            for cell in self.safes:
                if cell not in self.moves_made:
                    return cell
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves_and_mines = self.moves_made.union(self.mines)
        possible_mines = self.possible_mine()
        for i in range(self.height):
            for j in range(self.width):
                i = random.randrange(self.height)
                j = random.randrange(self.width)
                if (i, j) not in moves_and_mines.union(possible_mines):
                    return (i, j)
        # if all remaining choices are possible mines 
        if len(possible_mines) > 0:
            return possible_mines.random.choice()
        else:
            return None

    def possible_mine(self):
        """
        return a set of cells that may be mines
        """
        possible_mines = set()
        for sentence in self.knowledge:
            if sentence.count > 0:
                for cell in sentence.cells:
                    if cell not in self.mines:
                        possible_mines.add(cell)
        return possible_mines

    def ai_minesweeper_print(self):
        print("print Knowlegde ")
        for sentence in self.knowledge:
            # print(sentence.__str__())
            print(sentence.cells)
            print(sentence.count)
