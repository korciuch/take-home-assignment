#/usr/bin/env python3

import sys
from utils import Board, Coordinate, Shape, Lexicon

NEIGHBORS = [
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
            # mark starting coord as visited
            board.visited[starting_coord.r][starting_coord.c] = True
            # define starting string
            starting_str = board.values[starting_coord.r][starting_coord.c]
            # solve board - get all valid words from current board
            solve(board,starting_coord,starting_str,lexicon,results)
            # done collecting words at this starting coord
            # unmark as visited
            board.visited[starting_coord.r][starting_coord.c] = False
    print(results)
    return results

def solve(board: Board, curr_coord: Coordinate, curr_str: str, lexicon: Lexicon, positives: list) -> None:
    # FAILURE: no prefix exists, prune current search path
    if not lexicon.is_prefix(curr_str):
        return
    # SUCCESS: exact match, add to results
    elif curr_str in lexicon.words:
        positives.append(curr_str)
    # EXPLORE: expand search path to valid adjacent neighbors
    for n in NEIGHBORS:
        new_r = curr_coord.r + n.r
        new_c = curr_coord.c + n.c
        new_coord = Coordinate(new_r,new_c)
        if board.is_within_bounds(new_coord) and not board.is_visited(new_coord):
            board.mark_as_visited(new_coord)
            # if new coordinate is within bounds and hasn't been visited, append to search path
            curr_str += board.values[new_coord.r][new_coord.c]
            # push new stack frame
            solve(board,new_coord,curr_str,lexicon,positives)
            # backtrack
            board.unmark_as_visited(new_coord)
            curr_str = curr_str[:-1]
if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(
            random_seed=int(sys.argv[1]),
            shape=Shape(int(sys.argv[2]),int(sys.argv[3]))
        )
    else:
        print("Expected usage: python3 solve.py <random_seed> <num_rows> <num_columns>")