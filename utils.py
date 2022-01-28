# /usr/bin/env python3

import string
import numpy as np
from copy import deepcopy

# Defines 2D shape of a board

class Shape:
    def __init__(self, num_rows: int, num_columns: int):
        self.pair = tuple((num_rows, num_columns))
        self.width = num_columns
        self.height = num_rows


# Wrapper for a coordinate pair - row & column notation

class Coordinate:
    def __init__(self, row_component: int, column_component: int):
        self.pair = tuple((row_component, column_component))
        self.r = row_component
        self.c = column_component

    def __str__(self):
        return "Coordinate: ({},{})".format(self.r, self.c)


# Representation of a board's properties and visitor bookkeeping

class Board:
    LETTERS = list(string.ascii_lowercase)

    def __init__(self, random_seed: int, shape: Shape):
        np.random.seed(random_seed)
        self.values = np.random.choice(self.LETTERS, shape.pair, replace=True)
        self.visited = np.zeros(shape.pair, dtype=bool)
        self.shape = shape
        self.minR = 0
        self.maxR = self.shape.height - 1
        self.minC = 0
        self.maxC = self.shape.width - 1

    def is_within_bounds(self, coord: Coordinate) -> bool:
        if coord.r > self.maxR or coord.r < self.minR:
            return False
        elif coord.c > self.maxC or coord.c < self.minC:
            return False
        else:
            return True

    def is_visited(self, coord: Coordinate):
        return self.visited[coord.r][coord.c]

    def mark_as_visited(self, coord: Coordinate):
        self.visited[coord.r][coord.c] = True

    def unmark_as_visited(self, coord: Coordinate):
        self.visited[coord.r][coord.c] = False


# Ground truth for words that can be found on a board

class Lexicon:
    MIN_WORD_LENGTH = 3

    def __init__(self, infile: str):
        self.words = set()
        self.populate_dictionary(infile)

    def populate_dictionary(self, infile: str):
        with open(infile) as f:
            for l in f:
                word = l.split('\n')[0]
                if len(word) >= self.MIN_WORD_LENGTH:
                    self.words.add(word.lower())

    def is_prefix(self, s: str) -> bool:
        search = filter(lambda x: x.startswith(s), list(self.words))
        return len(list(search)) > 0


# Wrapper for the basic unit of work fed into the ProcessPoolExecutor

class WorkUnit():
    def __init__(self, starting_coord: Coordinate, starting_char: str, board: Board, lexicon: Lexicon):
        self.coord = starting_coord
        self.char = starting_char
        self.data = []
        self.board = deepcopy(board)

    def __str__(self):
        return "WorkUnit: {}, {}, {}, {}".format(self.char, self.coord, self.data, self.board.values)
