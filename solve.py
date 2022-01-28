# /usr/bin/env python3

import sys
import concurrent.futures
from utils import Board, Coordinate, Shape, Lexicon, WorkUnit

# List of all 8 possible neighbors in 2D space

NEIGHBORS = [
    Coordinate(-1, -1),
    Coordinate(-1, 0),
    Coordinate(-1, 1),
    Coordinate(0, -1),
    Coordinate(0, 1),
    Coordinate(1, -1),
    Coordinate(1, 0),
    Coordinate(1, 1),
]

def main(random_seed: int, shape: Shape) -> None:
    # create random board
    board = Board(random_seed=random_seed, shape=shape)
    print("BOARD: \n", board.values)
    # load in words for evaluation of the exploration algorithm
    lexicon = Lexicon('./words.txt')
    work_units = []
    for row in range(0, shape.height):
        for column in range(0, shape.width):
            # define starting coordinate
            starting_coord = Coordinate(row, column)
            # define starting string to pass into solve
            starting_char = board.values[starting_coord.r][starting_coord.c]
            board.mark_as_visited(starting_coord)
            unit = WorkUnit(starting_coord, starting_char, board, lexicon)
            board.unmark_as_visited(starting_coord)
            # append work units to list for multiprocessing
            work_units.append(unit)
    results = execute_work_units(work_units, lexicon)
    print("RESULTS: ", results)
    return results


# Multiprocessing: for each grid cell on board, call solve with corresponding
# context. Since the execution times of the depth-first search algorithm vary,
# we benefit from parallel over sequential execution.

def execute_work_units(work_units: list, lexicon: Lexicon) -> set:
    results = set()
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        future_to_unit = {
            executor.submit(solve, unit.board, unit.coord, unit.char, lexicon, unit.data):
            unit for unit in work_units
        }
        for future in concurrent.futures.as_completed(future_to_unit):
            result = future.result()
            if len(result) > 0:
                results.update(set(result))
    return results


# Depth first search: starting at an arbitrary point on the board, find
# all valid word combinations that originate from the starting coordinate.

def solve(board: Board, curr_coord: Coordinate, curr_str: str, lexicon: Lexicon, positives: list) -> None:
    # Failure: no prefix exists, prune current search path
    if not lexicon.is_prefix(curr_str):
        return
    # Success: exact string match, add to positive matches
    elif curr_str in lexicon.words and curr_str not in positives:
        positives.append(curr_str)
    # Explore: expand search path to valid adjacent neighbors
    for n in NEIGHBORS:
        new_r = curr_coord.r + n.r
        new_c = curr_coord.c + n.c
        new_coord = Coordinate(new_r, new_c)
        # don't go out of bounds or in already visited cell
        if board.is_within_bounds(new_coord) and not board.is_visited(new_coord):
            board.mark_as_visited(new_coord)
            curr_str += board.values[new_coord.r][new_coord.c]
            # push new recursive stack frame
            solve(board, new_coord, curr_str, lexicon, positives)
            # backtrack, options exhausted
            board.unmark_as_visited(new_coord)
            curr_str = curr_str[:-1]

    return positives


# Main entrypoint for solve.py

if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(
            random_seed=int(sys.argv[1]),
            shape=Shape(
                int(sys.argv[2]),
                int(sys.argv[3])
            )
        )
    else:
        print("Expected usage: python3 solve.py <random_seed> <num_rows> <num_columns>")
