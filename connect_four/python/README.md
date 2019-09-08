Official size: 
7 columns
6 rows

We assume that players and X (who moves first) and O.

https://en.wikipedia.org/wiki/Connect_Four

Example runs
============

$ time p board.py 
After 5000 games average game length = 21.409
real    0m1,097s

Todo next
=========

* Implement a evaluation function
* Implement a computer player
* Implement Alpha-beta with transposition tables
* Implement a GUI in React and a Flask API in Python

Lessons and ideas
=================

* Hash as an int compared to string saves 75% memory and a bit of time
* Unlimited memo even for 5x5 can easily take more than 4Gb of RAM. One needs to make a cut-off
* pypy3 uses more RAM than cpython
* pypy3 seems to be around 4x faster than cpython
* inlining the enum type (into a bool or int) doesn't help performance
* PERF: for cpython mutable vs immutable doesn't make a big difference,
        but for pypy3 the mutable version is 2-3 times faster at move
        generation.

Results
=======

Solving 4x4 (with pypy3)
a) directly [4m] 
   Total visited nodes = 131,060,741
b) with memo [0.8s]
    Total visited nodes = 161,029
c) with alphabeta [0.6s]~[1.6s]
    Total visited nodes = 62,889
d) with quick jumps [1m18s] (return when found a winning move)
    Total visited nodes = 50,624,601
e) with alpha-beta specialized for game solving [0.6s]
    Total visited nodes = 60,184
f) quick jumps combined with memoization [0.9s]
    Total visited nodes = 146,711
g) with alpha-beta specialized with memo: [0.35s]
    Total visited nodes = 11,766

Solving 4x5
a) directly: ???
b) with memo [8s]
    Total visited nodes = 1,745,379
c) with alphabeta [5s]
    Total visited nodes = 1,227,610
e) with alpha-beta specialized for game solving []
f) quick jumps combined with memoization [9s]
    Total visited nodes = 1,388,692
g) with alpha-beta specialized with memo: [2s]
    Total visited nodes = 94,633

Solving 5x4
a) directly: ???
b) with memo [18s]
    Total visited nodes = 4,009,175
c) with alphabeta [33s]
    Total visited nodes = 18,026,614
e) with alpha-beta specialized for game solving [36s]
    Total visited nodes = 17,915,470
f) quick jumps combined with memoization [19s]
    Total visited nodes = 3,033,075
g) with alpha-beta specialized with memo: [2s]
    Total visited nodes = 508,120

Solving 5x5 (with pypy3)
a) directly ???
b) memo: [18m] - with memo with a cutoff at 20 [21 leads to memory error]
    Total visited nodes = 668,607,278
c) with alphabeta [43m] 
    Total visited nodes = 2,135,732,339
f) quick jumps combined with memoization []
g) with alpha-beta specialized with memo: [21s]
    Total visited nodes = 7,952,955

Solving 6x4
g) with alpha-beta specialized with memo: [1m]
    Game solved. Result = -1
    Total visited nodes = 21,968,555

Solving 4x6
g) with alpha-beta specialized with memo: [2s]
    Game solved. Result = 0
    Total visited nodes = 626,341

Solving 5x6
g) with alpha-beta specialized with memo: [2.8m]
    Game solved. Result = 0
    Total visited nodes = 74,136,492
    Total time: 2.83m

Solving 6x5
g) with alpha-beta specialized with memo: []
    visited 101M nodes [15.11%] in 4.65m
    MemoryError 

Solving 6x6
g) with alpha-beta specialized with memo: []

Solving 7x6
