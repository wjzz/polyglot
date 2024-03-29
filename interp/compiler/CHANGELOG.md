2019/10/22

* implemented early jumps for `return`

`return` should jump to the function epilogue. We want the lexically closest one,
so keeping a stack of the epilogue labels is enough.

* implemented `break` and `continue`

This is very similar to `return`, but this time we look at loop labels instead of function labels.
Since `break` jumps to the loop_end label and `continue` jumps to the loop_start label we keep
a stack of loop [start, end] label pairs.

* tabs in source code are allowed

* removed the old syntax (python-like top-level statements instead of c-style main function)

* removed the old AST-based tests (there were used when there was no parser)

* removed many unused files, including a while-interpreter (I was not maintaining it anyways)

* BUG: my implementation of local variables was *very* naive and thus incorrect. Locals have to be put on the stack along with parameters - otherwise recursive functions won't work properly!

* implemented putting local variables on the stack.
I made the same mistake again - to allocate more memory we have to *substract* from rsp, not add - the stack grows downwards here!
Also it's important to always remember that we use a stack so if we allocate stuff, then we have to deallocate in the reverse order.

* implemented variable renaming - this way we get block scoping for free, without having to manage another stack for that

2019/10/23

* extended StmDecl with a flag to denote if the variable is local, global or static

* implemented global variables again. Static variables are not handled yet.

* generalized atomic types to CType (normal==atomic or pointer type)

* added arith unary ops (* and &) and ArithUnaryop constructor

* StmAssign now takes a lvalue instead of var

* implemented simple pointer operations: & and *

* Addresses are now stored as VarAddr

First I made a hack - I stored variable addresses as `rbp - 8 * 3`, but it was not possible to write
`mov rax, rbp - 8 * 3` => we had to do the calculations in assembly.

* Pointers can now change values, `*n = 5;` works

* Pointers as function parameters work out of the box! :)

* We can now use pointers to change function parameters values.

* Move assignment from Stm to Expr. This complicates the parser a little bit.

* Include all expressions in statements. The code generator for `a;`
calculates `a` and then pops the stack (we don't use the value).

2019/10/25

* upgrade to python 3.8

* install coverage (wasn't easy! because I have many versions of python installed, it only works with `pyenv` for me).
* Add `make cov` to the main makefile

* install `pylint`:
- trim trailing whitespace on save

* install `flake8`:
