data BinOp = Sum | Mul deriving (Show, Eq)

data Expr = Lit Int | Bin BinOp Expr Expr deriving (Show, Eq)

interp :: BinOp -> (Int -> Int -> Int)
interp Sum = (+)
interp Mul = (*)

eval :: Expr -> Int
eval (Lit n) = n
eval (Bin op e1 e2) = eval e1 `fop` eval e2 where
  fop = interp op

depth :: Expr -> Int
depth (Lit _) = 1
depth (Bin _ e1 e2) = 1 + (depth e1 `max` depth e2)

mycycle :: a -> [a]
mycycle a = a : mycycle a

mycycle2 :: a -> [a]
mycycle2 x = let xs = mycycle2 x in x : xs
