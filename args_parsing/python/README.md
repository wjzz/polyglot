Oficial documentation:
======================

https://docs.python.org/3/library/argparse.html

My example:
===========

```
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

    parser.add_argument('--mutable', dest='mutable', type=bool, nargs="?",
                    const=True, default=False,
                    help='use mutable operations (default: immutable)')

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

```
