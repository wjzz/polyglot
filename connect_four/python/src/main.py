from board import Board, Config
import traversals as trav
from utils import humanize_time, Timer

import argparse

# trav.traverse_all_immutable
def calculate_num_nodes(generator):
    def fun(board, depth):
        return sum(1 for _ in generator(board, depth))
    return fun

def main(*, cols, rows, depth, start, end, generator):
    Config.COLS = cols
    Config.ROWS = rows
    if depth is None:
        depth = cols * rows
    if start is None and end is None:
        start = end = depth
    elif start is None:
        start = 0
    elif end is None:
        end = depth

    for depth in range(start, end+1):
        board = Board()

        print(f"Starting search for size {Config.COLS} x {Config.ROWS} at depth {depth}", end="")
        timer = Timer()
        with timer:
            total = generator(board, depth)
            # total = calculate_num_nodes(board, depth)
            # total = trav.count_all_top(board, depth)

        milion_nodes_per_sec = total / (1000000 * timer.seconds)  
        print(f"\rDepth {depth:2}: {total:13,} "
            f"[{milion_nodes_per_sec:.2f} M nodes per sec] [{str(timer)}]"
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
        'Run benchmarks on Connect Four implementations')

    parser.add_argument('cols', metavar='COLS', type=int, default=4, nargs="?",
                    help='width of the board (default = 4)')

    parser.add_argument('rows', metavar='ROWS', type=int, default=4, nargs="?",
                    help='height of the board (default = 4)')

    parser.add_argument('--depth', type=int, default=None, nargs="?", 
                    help="search depth (default = None)")
    parser.add_argument('--start', type=int, default=None, nargs="?", 
                    help="start depth (default = None)")
    parser.add_argument('--end', type=int, default=None, nargs="?",
                    help="end depth (depth = None)")

    parser.add_argument('--generator', dest='generator', type=bool, nargs="?",
                    const=True, default=False,
                    help='use a generator (default: dedicated traversal)')

    parser.add_argument('--memo', dest='memo', type=bool, nargs="?",
                    const=True, default=False,
                    help='use memoization for nodes (default: no memo)')

    args = parser.parse_args()

    print(f"COLS = {args.cols}")
    print(f"ROWS = {args.rows}")
    print(f"GENERATOR = {args.generator}")
    print(f"MEMO = {args.memo}")
    print(f"DEPTH = {args.depth}")
    print(f"START = {args.start}")
    print(f"END = {args.end}")

    if args.memo:
        if args.generator:
            generator = calculate_num_nodes(trav.traverse_unique_immutable)
        else:
            generator = trav.count_all_unique_top
    else:
        if args.generator:
            generator = calculate_num_nodes(trav.traverse_all_immutable)
        else:
            generator = trav.count_all_top

    print(f"generator fun = {generator.__qualname__}")

    main(
        cols = args.cols, 
        rows = args.rows,
        depth = args.depth,
        start = args.start,
        end = args.end,
        generator = generator,
    )
