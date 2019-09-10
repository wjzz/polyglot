import unittest
from expr import NumberLit, Variable, Op, BinaryOp, LetIn
from lexer import tokenize, simplify
from parser import parse
from evaluator import evaluate
from top import ev

class Tests(unittest.TestCase):
    def test_expr_str(self):
        n = NumberLit(11)
        m = NumberLit(22)
        self.assertEqual(str(n), "11")
        self.assertEqual(str(m), "22")
        x = Variable("x")
        self.assertEqual(str(x), "x")
        e1 = BinaryOp(n, Op.Plus, m)
        self.assertEqual(str(e1), "(11 + 22)")
        e2 = BinaryOp(n, Op.Mult, m)
        self.assertEqual(str(e2), "(11 * 22)")
        e3 = BinaryOp(e1, Op.Mult, e1)
        self.assertEqual(str(e3), "((11 + 22) * (11 + 22))")
        y = Variable("y")
        self.assertEqual(str(y), "y")
        e4 = BinaryOp(x, Op.Plus, y)
        self.assertEqual(str(e4), "(x + y)")
        e5 = LetIn("x", n, x)
        self.assertEqual(str(e5), "(let x := 11 in x)")
        e6 = LetIn("x", n, BinaryOp(x, Op.Plus, x))
        self.assertEqual(str(e6), "(let x := 11 in (x + x))")

    def test_lexer(self):
        e1 = "1"
        self.assertEqual(list(simplify(tokenize(e1))),
            [('NUMBER', 1), 'EOF'])
        
        input_str = "(1 + 11 * 22)"

        result = list(simplify(tokenize(input_str)))

        expected = ['LPAREN', ('NUMBER', 1), 'PLUS', ('NUMBER', 11), 
            'TIMES', ('NUMBER', 22), 'RPAREN', 'EOF']
        
        self.assertEqual(expected, result)

    def test_lexer_with_let(self):
        input_str = "let x := 1 in x + x end"

        result = list(simplify(tokenize(input_str)))

        expected = ['LET', ('ID', "x"), "ASSIGN", ('NUMBER', 1), "IN", 
            ('ID', "x"), 'PLUS', ('ID', "x"), 'END', 'EOF']
        
        self.assertEqual(expected, result)

    def test_parser(self):
        e1 = "1"
        self.assertEqual(parse(e1), NumberLit(1))

        e2 = "(1)"
        self.assertEqual(parse(e2), NumberLit(1))

        e3 = "((1))"
        self.assertEqual(parse(e3), NumberLit(1))

        e4 = "(1 + 2)"
        r4 = BinaryOp(
                NumberLit(1),
                Op.Plus,
                NumberLit(2))
        self.assertEqual(parse(e4), r4)

        e5 = "1 + 2"
        self.assertEqual(parse(e5), r4)

        e6 = "(1 * 2)"
        r6 = BinaryOp(
                NumberLit(1),
                Op.Mult,
                NumberLit(2))
        self.assertEqual(parse(e6), r6)

        e7 = "1 * 2"
        self.assertEqual(parse(e7), r6)

        e8 = "1 + 2 * 3"
        r8 = BinaryOp(
                NumberLit(1),
                Op.Plus,
                BinaryOp(
                    NumberLit(2),
                    Op.Mult,
                    NumberLit(3)
                ))
        self.assertEqual(parse(e8), r8)

        e9 = "let x := 1 in x end"
        r9 = LetIn(
                "x",
                NumberLit(1),
                Variable("x")
                )
        self.assertEqual(parse(e9), r9)

        e10 = "2 + let x := 1 in x end"
        r10 = BinaryOp(
                NumberLit(2),
                Op.Plus,
                LetIn(
                    "x",
                    NumberLit(1),
                    Variable("x")
                ))
        self.assertEqual(parse(e10), r10)

        e11 = "let x := 1 in x + 2 end"
        r11 = LetIn(
                "x",
                NumberLit(1),
                BinaryOp(
                    Variable("x"),
                    Op.Plus,
                    NumberLit(2)
                ))
        self.assertEqual(parse(e11), r11)

        e12 = "let x := 1 in x end + 2"
        r12 = LetIn(
                "x",
                NumberLit(1),
                BinaryOp(
                    Variable("x"),
                    Op.Plus,
                    NumberLit(2)
                ))
        self.assertEqual(parse(e12), r12)


    def test_evaluator(self):
        n = NumberLit(2)
        m = NumberLit(3)
        self.assertEqual(evaluate(n), 2)
        self.assertEqual(evaluate(m), 3)
        e1 = BinaryOp(n, Op.Plus, m)
        self.assertEqual(evaluate(e1), 5)
        e2 = BinaryOp(n, Op.Mult, m)
        self.assertEqual(evaluate(e2), 6)
        e3 = BinaryOp(e1, Op.Mult, e1)
        self.assertEqual(evaluate(e3), 25)

    def test_everything_together(self):
        def test(a, b):
            self.assertEqual(ev(a), b)

        test("1", 1)
        test("1 + 1", 2)
        test("1+2+3+4", 10)
        test("1 + 1 + 1 + 1", 4)
        test("2 + 2 * 2", 6)
        test("(2 + 2) * 2", 8)
        test("2 * 2 + 2", 6)
        test("(2 + 2) * (2 + 2)", 16)
        test("2+2*2+2", 8)
        test("let x := 1 in x + x end", 2)
        test("let z := 2 in z * z end", 4)
        test("let x := 2 in (let y := 3 in x + y end) end", 5)

if __name__ == "__main__":
    unittest.main()
