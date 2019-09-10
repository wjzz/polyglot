The goal of this task is to write an interpreter for the simplest expression language extended with let bindings.

Part of the task is writing a lexer and a parser. 

Abstract syntax:

type Var = String
type Op = Plus | Mult
type Expr = Num int | Var Var | Let Var Expr Expr | Binary Op Expr Expr

Concrete syntax (including parenthesis and additional rules):

e ::= NUMBER | VAR | (e) | e + e | e * e | LET x := e in e END

To specify the parse and to enable testing without evaluating expressions 
we introduce the following function (in pseudo Haskell+JS):

```
canonical (Num n) = n.toString()
canonical (Var v) = v
canonical (Let v e1 e2) = `({let ${v} := ${s1} in ${s2})` where
  s1 = canonical e1
  s2 = canonical e2

canonical (Binary op e1 e2) = `(${s1} ${sop} ${s2})` where
  s1 = canonical e1
  sop = op.toString()
  s2 = canonical e2
```

We abreviate it as `can` below.

Parsing rules: 

- extra whitespace is allowed, just like extra parens are OK.

- multiplication binds stronger than addition, e.g.

can $ parse "2 + 2 * 2" ==> "(2 + (2 * 2))"

- both operators are right-associative, e.g.

can $ parse "2 + 2 + 2" ==> "(2 + (2 + 2))"
can $ parse "2 * 2 * 2" ==> "(2 * (2 * 2))"

=============
Inputs:
=============

Your program should have accept two modes: parsing and evaluation. 
You don't have to worry about integer overflow.

=============
Outputs:
=============

One line with the correct result

============
Examples:
============

```
$ PROGRAM --parse
2 + 2 * 2<ENTER><EOF>
```
should print 
```
(2 + (2 * 2))
```

while

```
$ PROGRAM --eval
2 + 2 * 2<ENTER><EOF>
```
should print 
```
6
```

```
$ PROGRAM --eval
let x := 2 + 2 in x + x end<ENTER><EOF>
```
should print 
```
8
```

