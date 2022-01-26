#/usr/bin/env python3

import sys
from utils import Board, Coordinate, Shape, Lexicon

VECTORS = [
    Coordinate(-1,-1),
    Coordinate(-1,0),
    Coordinate(-1,1),
    Coordinate(0,-1),
    Coordinate(0,1),
    Coordinate(1,-1),
    Coordinate(1,0),
    Coordinate(1,1),
]

def main(random_seed: int, shape: Shape) -> None :
    results = []
    # create random board
    board = Board(random_seed=random_seed,shape=shape)
    print(board.values)
    # load in words for evaluation of the exploration algorithm
    lexicon = Lexicon('./words.txt')
    for row in range(0,shape.height):
        for column in  range(0,shape.width):
            # define starting coordinate for depth first search
            starting_coord = Coordinate(row,column)
            # define starting string
            starting_str = board.values[starting_coord.r][starting_coord.c]
            # solve board - get all valid words from current board
            solve(board,starting_coord,starting_str,lexicon,results)
    print(results)
    return results

def solve(board: Board, curr_coord: Coordinate, curr_str: str, lexicon: Lexicon, positives: list) -> None:
    # see if words can be made with current prefix
    possible_words = list(filter(lambda x: x.startswith(curr_str), list(lexicon.words)))
    # FAILURE: no prefix exists, prune current search path
    if len(possible_words) == 0:
        return
    # SUCCESS: exact match, add to results
    elif curr_str in lexicon.words:
        print(curr_str)
        positives.append(curr_str)
    # EXPLORE: expand search path to valid adjacent neighbors
    for v in VECTORS:
        new_r = curr_coord.r + v.r
        new_c = curr_coord.c + v.c
        new_coord = Coordinate(new_r,new_c)
        if board.is_within_bounds(new_coord) and not board.is_visited(new_coord):
            # if new coordinate is within bounds and hasn't been visited, append to search path
            board.mark_as_visited(new_coord)
            curr_str += board.values[new_coord.r][new_coord.c]
            # push new stack frame
            solve(board,new_coord,curr_str,lexicon,positives)
            # backtrack once all possibilites evaluated
            board.unmark_as_visited(new_coord)

if __name__ == '__main__':
    if len(sys.argv) !=  4:
        print("Expected usage: python3 solve.py random_seed num_rows num_columns")
    else:
        main(
            random_seed=int(sys.argv[1]),
            shape=Shape(int(sys.argv[2]),int(sys.argv[3]))
        )