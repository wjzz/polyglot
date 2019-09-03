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

Results
=======

Solving 4x4 (with pypy3)
a) directly [4m] 
   Total visited nodes = 131,000,000
b) with memo [0.8s]
    Total visited nodes = 161,029
c) with alphabeta [1.6s]
    Total visited nodes = 62,889

Solving 4x5
a) directly: ???
b) with memo [8s]
    Total visited nodes = 1,745,379
c) with alphabeta [5s]
    Total visited nodes = 1,227,610

Solving 5x4
b) with memo [18s]
    Total visited nodes = 4,009,175
c) with alphabeta [33s]
    Total visited nodes = 18,026,614

Solving 5x5 (with pypy3)
a) directly ???
b) memo: [18m] - with memo with a cutoff at 20 [21 leads to memory error]
    Total visited nodes = 668,607,278
c) with alphabeta [43m] 
    Total visited nodes = 2,135,732,339
