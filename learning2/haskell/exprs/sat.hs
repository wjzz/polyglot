data Atom = Lit Bool | Var Var Bool

data Sat3Clause = [Atom] -- this should have size 3

data Sat3Expr = [Sat3Clause]
