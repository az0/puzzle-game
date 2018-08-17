# Generates random boards for Fat Brain's puzzle game AnimalLogic,
# and then it solves each puzzle.
#
# In the game, animals cross the river to the safety zone, and the restriction
# is each animal must match the next based on color or species.
#
# https://www.fatbraintoys.com/toy_companies/fat_brain_toy_co/animalogic.cfm
#
#
# By Andrew Ziem, May 2018

# constants for Display Mode
DM_CSV = 1
DM_VERBOSE = 2


class Animal:
    """Represents an animal, which is a game piece"""

    def __init__(self, species, color):
        """Initialize the animal"""
        self.species = species
        self.color = color

    def __str__(self):
        """Returns a string that identifies the animal"""
        pretty_species = {'g': 'giraffe',
                          'h': 'hippo', 'l': 'lion', 'c': 'camel'}
        pretty_color = {'r': 'red', 'g': 'green', 'b': 'blue', 'y': 'yellow'}
        return '%s %s' % (pretty_color[self.color], pretty_species[self.species])

    def __repr__(self):
        return str(self)

    def is_match(self, another_animal):
        """Check whether this animal matches another on color or species"""
        # Are these the same species?
        if self.species == another_animal.species:
            # They are the same species, so they are a match.
            return True

        if self.color == another_animal.color:
            return True

        return False


class Board:

    def __init__(self):
        self.board = dict.fromkeys([0, 1, 2, 3])

    def str_row(self, row_number, separator):
        """Return a string representing a row on the board"""
        assert(0 <= row_number <= 3)
        row_animals = self.board[row_number]
        return separator.join([str(animal) for animal in row_animals])

    def __str__(self):
        """Return a string representing the whole board"""
        row_str = ''
        # loop through all rows
        for row_number in [0, 1, 2, 3]:
            # show the row number
            row_str += 'row %d: ' % (row_number + 1)
            # animals
            row_str += self.str_row(row_number, '\t')
            # add line break
            row_str = row_str + '\n'
        return row_str

    def count(self):
        count = 0
        for row in [0, 1, 2, 3]:
            #print('row count=',len(self.board[row]))
            for animal in self.board[row]:
                count = count + 1
        return count

    def make_random_board(self):
        """Put all pieces on the board with random positions"""
        # Fill a list with 16 animals in a deterministic order.
        linear_board = []
        for color in ['r', 'g', 'b', 'y']:
            for species in ['g', 'h', 'l', 'c']:
                a = Animal(species, color)
                linear_board.append(a)
        # Shuffle the list.
        import random
        random.shuffle(linear_board)
        # Transform the single list to four row.
        for row in [0, 1, 2, 3]:
            self.board[row] = linear_board[-4:]
            del linear_board[-4:]


def solve_board(safety_zone, board, solution_counter):
    """
    Solve the game board using a recursive strategy

    safety_zone: the current partial or full solution as a list of animals

    board: the current game board (with zero to 16 pieces)

    solution_counter: the number of solutions found so far
    """
    #print('solve_board(%s, %s)' % (safety_zone, board))
    if not 16 == (board.count() + len(safety_zone)):
        print('board count = %d, safety zone count = %d' %
              (board.count(), len(safety_zone)))
        raise RuntimeError('the count of pieces is not 16')
    if len(safety_zone) == 16:
        # found solution
        #print('solution = ', safety_zone)
        return 1 + solution_counter
    # check each row
    for row in range(0, 4):
        if not board.board[row]:
            # This row is empty, so check the next row.
            continue
        board_copy = Board()
        board_copy.board = {}
        for row_copy in range(0, 4):
            # this is dramatically faster than copy.deepcopy()
            board_copy.board[row_copy] = board.board[row_copy].copy()
        assert(board.count() == board_copy.count())
        chosen_animal = board_copy.board[row].pop(0)
        if not safety_zone or safety_zone[-1].is_match(chosen_animal):
            # found valid move
            # valid possibility 1: The safety zone was empty.
            # valid possibility 2: The chosen animal matches the last animal
            # in the safety zone.
            solution_counter = solve_board(
                safety_zone + [chosen_animal, ], board_copy, solution_counter)
    return solution_counter


def print_csv_line(board, solution_count):
    """Show the initial game board and solution count in CSV format"""
    for row_i in range(0, 4):
        print(board.str_row(row_i, ';'), end=",")
    print(solution_count)


def go():
    display_mode = DM_CSV
    import sys
    if '--verbose' in sys.argv:
        display_mode = DM_VERBOSE
    # create empty board
    b = Board()
    if display_mode == DM_CSV:
        print('row_1,row_2,row_3,row_4,solution_count')
    for i in range(0, 10000):
        # add animals at random
        b.make_random_board()
        if display_mode == DM_VERBOSE:
            print(b)
        assert(16 == b.count())
        solution_count = solve_board([], b, 0)
        if display_mode == DM_VERBOSE:
            print('solution count=', solution_count)
        else:
            print_csv_line(b, solution_count)

go()


# Exercise for the reader:
# Determine the number of solutions for the games provided in the
# official game manual.
