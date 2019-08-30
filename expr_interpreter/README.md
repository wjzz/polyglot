The goal of this task is to write an interpreter for the simplest expression language.

Part of the task is writing a lexer and a parser. 

Abstract syntax:

type Op = Plus | Mult
type Expr = Num int | Binary Op Expr Expr

Concrete syntax (including parenthesis and additional rules):

e ::= NUMBER | (e) | e + e | e * e


To specify the parse and to enable testing without evaluating expressions 
we introduce the following function (in pseudo Haskell+JS):

```
canonical (Num n) = n.toString()
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

