import unittest

from ast import *
from lexer import tokenize, simplify
from parser import parse_file, parse_stm, parse_expr, parse_arith
import code_generator
from local_vars import get_local_vars
from rename import rename_vars

class LexerTests(unittest.TestCase):
    def test_lexer(self):
        e1 = "1"
        self.assertEqual(list(simplify(tokenize(e1))),
            [('NUMBER', 1), 'EOF'])

        input_str = "(1 + 11 * 22)"

        result = list(simplify(tokenize(input_str)))

        expected = ['LPAREN', ('NUMBER', 1), 'PLUS', ('NUMBER', 11),
            'TIMES', ('NUMBER', 22), 'RPAREN', 'EOF']

        self.assertEqual(expected, result)

    def test_lexer_comment(self):
        input_str = "// this is a comment\n+"
        result = list(simplify(tokenize(input_str)))

        expected = [ 'PLUS', 'EOF' ]

        self.assertEqual(expected, result)

    def test_lexer_ident(self):
        inputs = [
            ("x",
            [('ID', 'x'), 'EOF']),
            ("x123",
            [('ID', 'x123'), 'EOF']),
            ("x_123",
            [('ID', 'x_123'), 'EOF']),

        ]
        for (input, expected) in inputs:
            with self.subTest(input=input):
                self.assertEqual(
                    list(simplify(tokenize(input))),
                    expected)

    def test_lexer_decl(self):
        input = "long x"
        result = [('TYPE', 'long'), ('ID', 'x'), 'EOF']
        self.assertEqual(
            list(simplify(tokenize(input))),
            result)

    def test_lexer_decl_pointers(self):
        inputs = [
            ("int* d",
                [('TYPE', 'int'), 'TIMES', ('ID', 'd'), 'EOF']),
            ("int *d",
                [('TYPE', 'int'), 'TIMES', ('ID', 'd'), 'EOF']),
            ("long* d",
                [('TYPE', 'long'), 'TIMES', ('ID', 'd'), 'EOF']),
        ]
        for (input, expected) in inputs:
            with self.subTest(input=input):
                self.assertEqual(
                    list(simplify(tokenize(input))),
                    expected)

    def test_lexer_address(self):
        inputs = [
            ("d = &n",
                [('ID', 'd'), 'EQUAL', 'AMPERSAND', ('ID', 'n'), 'EOF']),
        ]
        for (input, expected) in inputs:
            with self.subTest(input=input):
                self.assertEqual(
                    list(simplify(tokenize(input))),
                    expected)

    def test_lexer_ops(self):
        inputs = [
            ("x == 0",
                [('ID', 'x'), 'DBL_EQ', ('NUMBER', 0), 'EOF']),
            ("x != 0",
                [('ID', 'x'), 'NOT_EQ', ('NUMBER', 0), 'EOF']),
            ("x >= 0",
                [('ID', 'x'), 'GREATER_EQ', ('NUMBER', 0), 'EOF']),
            ("x > 0",
                [('ID', 'x'), 'GREATER', ('NUMBER', 0), 'EOF']),
            ("x <= 0",
                [('ID', 'x'), 'LESS_EQ', ('NUMBER', 0), 'EOF']),
            ("x < 0",
                [('ID', 'x'), 'LESS', ('NUMBER', 0), 'EOF']),
            ("! (x == 0)",
                ['BANG', 'LPAREN', ('ID', 'x'), 'DBL_EQ',
                    ('NUMBER', 0), 'RPAREN', 'EOF']),
        ]
        for (input, expected) in inputs:
            with self.subTest(input=input):
                self.assertEqual(
                    list(simplify(tokenize(input))),
                    expected)

    def test_lexer_while(self):
        input_str = "while (x > 0) { x = 10; } "

        result = list(simplify(tokenize(input_str)))

        expected = ['WHILE', 'LPAREN', ('ID', 'x'),
                   'GREATER', ('NUMBER', 0), 'RPAREN',
                   'LBRACE', ('ID', 'x'), 'EQUAL', ('NUMBER', 10),
                   'SEMI', 'RBRACE', 'EOF']

        self.assertEqual(expected, result)

    def test_lexer_if(self):
        input_str = "if (x > 0) { x = 10; } else { x = 5; }"

        result = list(simplify(tokenize(input_str)))

        expected = ['IF', 'LPAREN', ('ID', 'x'),
                   'GREATER', ('NUMBER', 0), 'RPAREN',
                   'LBRACE', ('ID', 'x'), 'EQUAL', ('NUMBER', 10),
                   'SEMI', 'RBRACE', 'ELSE',
                   'LBRACE', ('ID', 'x'), 'EQUAL', ('NUMBER', 5),
                   'SEMI', 'RBRACE', 'EOF']

        self.assertEqual(expected, result)

    def test_lexer_binops(self):
        input_str = "x && y || z"

        result = list(simplify(tokenize(input_str)))

        expected = [ ('ID', 'x'), 'AND', ('ID', 'y'),
                     'OR', ('ID', 'z'), 'EOF']

        self.assertEqual(expected, result)

    def test_lexer_fun_decl(self):
        input_str = "void foo(long a, int b, char c) { }"

        result = list(simplify(tokenize(input_str)))

        expected = [ ('TYPE', 'void'), ('ID', 'foo'),
            'LPAREN', ('TYPE', 'long'),
            ('ID', 'a'), 'COMMA', ('TYPE', 'int'), ('ID', 'b'),
            'COMMA', ('TYPE', 'char'), ('ID', 'c'),
            'RPAREN', 'LBRACE', 'RBRACE', 'EOF'
        ]

        self.assertEqual(expected, result)

    def test_lexer_incorrect_char(self):
        input_str = "\b"

        with self.assertRaises(Exception):
            list(simplify(tokenize(input_str)))

    def test_lexer_break(self):
        input_str = "break;"

        result = list(simplify(tokenize(input_str)))

        expected = ['BREAK', 'SEMI', 'EOF']

        self.assertEqual(expected, result)

    def test_lexer_continue(self):
        input_str = "continue;"

        result = list(simplify(tokenize(input_str)))

        expected = ['CONTINUE', 'SEMI', 'EOF']

        self.assertEqual(expected, result)

    def test_lexer_return(self):
        input_str = "return x;"

        result = list(simplify(tokenize(input_str)))

        expected = ['RETURN', ('ID', 'x'), 'SEMI', 'EOF']

        self.assertEqual(expected, result)

    def test_lexer_print(self):
        input_str = "print(x);"

        result = list(simplify(tokenize(input_str)))

        expected = ['PRINT', 'LPAREN', ('ID', 'x'),
                   'RPAREN', 'SEMI', 'EOF']

        self.assertEqual(expected, result)

    def test_lexer_compound_assign(self):
        inputs = [
            ("x += 1",
            [('ID', 'x'), 'PLUS_EQ', ('NUMBER', 1), 'EOF']),
            ("x -= 1",
            [('ID', 'x'), 'MINUS_EQ', ('NUMBER', 1), 'EOF']),
            ("x *= 1",
            [('ID', 'x'), 'TIMES_EQ', ('NUMBER', 1), 'EOF']),
            ("x /= 1",
            [('ID', 'x'), 'DIVIDE_EQ', ('NUMBER', 1), 'EOF']),
            ("x %= 1",
            [('ID', 'x'), 'MOD_EQ', ('NUMBER', 1), 'EOF']),
        ]

        for (input, expected) in inputs:
            with self.subTest(input=input):
                self.assertEqual(
                    list(simplify(tokenize(input))),
                    expected)

class ParserTests(unittest.TestCase):

    def test_parser_expr(self):
        v1 = "x"
        self.assertEqual(parse_arith(v1), Var("x"))

        v2 = "(x)"
        self.assertEqual(parse_arith(v2), Var("x"))

        v3 = "thisisalongvariable"
        self.assertEqual(parse_arith(v3), Var(v3))

        e1 = "1"
        self.assertEqual(parse_arith(e1), ArithLit(1))

        e2 = "(1)"
        self.assertEqual(parse_arith(e2), ArithLit(1))

        e3 = "((1))"
        self.assertEqual(parse_arith(e3), ArithLit(1))

        e4 = "(1 + 2)"
        r4 = ArithBinop(
                ArithOp.Add,
                ArithLit(1),
                ArithLit(2))
        self.assertEqual(parse_arith(e4), r4)

        e5 = "1 + 2"
        self.assertEqual(parse_arith(e5), r4)

        e6 = "(1 * 2)"
        r6 = ArithBinop(
                ArithOp.Mul,
                ArithLit(1),
                ArithLit(2))
        self.assertEqual(parse_arith(e6), r6)

        e7 = "1 * 2"
        self.assertEqual(parse_arith(e7), r6)

        e8 = "1 + 2 * 3"
        r8 = ArithBinop(
                ArithOp.Add,
                ArithLit(1),
                ArithBinop(
                    ArithOp.Mul,
                    ArithLit(2),
                    ArithLit(3)
                ))
        self.assertEqual(parse_arith(e8), r8)

        e9 = "(1 - 2)"
        r9 = ArithBinop(
                ArithOp.Sub,
                ArithLit(1),
                ArithLit(2))
        self.assertEqual(parse_arith(e9), r9)

        e10 = "(1 / 2)"
        r10 = ArithBinop(
                ArithOp.Div,
                ArithLit(1),
                ArithLit(2))
        self.assertEqual(parse_arith(e10), r10)

        e11 = "(1 % 2)"
        r11 = ArithBinop(
                ArithOp.Mod,
                ArithLit(1),
                ArithLit(2))
        self.assertEqual(parse_arith(e11), r11)

    def test_parser_expr_funcall(self):
        e1 = "foo()"
        r1 = FunCall("foo", [])
        self.assertEqual(parse_expr(e1), r1)

        e2 = "foo(1)"
        r2 = FunCall("foo", [ArithLit(1)])
        self.assertEqual(parse_expr(e2), r2)

        e3 = "foo(1,2)"
        r3 = FunCall("foo", [ArithLit(1), ArithLit(2)])
        self.assertEqual(parse_expr(e3), r3)

        e4 = "2 + foo()"
        r4 = ArithBinop(ArithOp.Add,
            ArithLit(2),
            FunCall("foo", []))
        self.assertEqual(parse_expr(e4), r4)

        e5 = "2 + foo() > 4"
        r5 = BoolArithCmp(ArithCmp.Gt, r4, ArithLit(4))
        self.assertEqual(parse_expr(e5), r5)

        e6 = "foo(x, y, bar())"
        r6 = FunCall("foo",
                [Var("x"),
                Var("y"),
                FunCall("bar", [])])
        self.assertEqual(parse_expr(e6), r6)

    def test_parser_bool_expr(self):
        b1a = "(x == 1)"
        self.assertEqual(parse_expr(b1a),
            BoolArithCmp(
                ArithCmp.Eq,
                Var("x"),
                ArithLit(1)))

        b4 = "(x > 1) && (y < 0)"
        self.assertEqual(parse_expr(b4),
            BoolBinop(
                BoolOp.And,
                BoolArithCmp(
                    ArithCmp.Gt,
                    Var("x"),
                    ArithLit(1)),
                BoolArithCmp(
                    ArithCmp.Lt,
                    Var("y"),
                    ArithLit(0))))

        b4a = "x > 1 && y < 0"
        self.assertEqual(parse_expr(b4a),
            BoolBinop(
                BoolOp.And,
                BoolArithCmp(
                    ArithCmp.Gt,
                    Var("x"),
                    ArithLit(1)),
                BoolArithCmp(
                    ArithCmp.Lt,
                    Var("y"),
                    ArithLit(0))))

        b5 = "(x > 1) || (y < 0)"
        self.assertEqual(parse_expr(b5),
            BoolBinop(
                BoolOp.Or,
                BoolArithCmp(
                    ArithCmp.Gt,
                    Var("x"),
                    ArithLit(1)),
                BoolArithCmp(
                    ArithCmp.Lt,
                    Var("y"),
                    ArithLit(0))))

        b5a = "x > 1 || y < 0"
        self.assertEqual(parse_expr(b5a),
            BoolBinop(
                BoolOp.Or,
                BoolArithCmp(
                    ArithCmp.Gt,
                    Var("x"),
                    ArithLit(1)),
                BoolArithCmp(
                    ArithCmp.Lt,
                    Var("y"),
                    ArithLit(0))))

    def test_parse_expr_pointers(self):
        inputs = [
            ("*n + 1",
                ArithBinop(
                    ArithOp.Add,
                    ArithUnaryop(
                        ArithUnaryOp.Deref,
                        Var("n")),
                    ArithLit(1)
                )),
            ("1 + *n",
                ArithBinop(
                    ArithOp.Add,
                    ArithLit(1),
                    ArithUnaryop(
                        ArithUnaryOp.Deref,
                        Var("n"))
                )),
            ("*n + *m",
                ArithBinop(
                    ArithOp.Add,
                    ArithUnaryop(
                        ArithUnaryOp.Deref,
                        Var("n")),
                    ArithUnaryop(
                        ArithUnaryOp.Deref,
                        Var("m"))
                ))
        ]

        for (input, expected) in inputs:
            with self.subTest(input=input):
                self.assertEqual(
                    parse_expr(input),
                    expected)

    def test_parser_expr_deref(self):
        input = "&n"

        self.assertEqual(parse_expr(input),
            ArithUnaryop(
                ArithUnaryOp.Addr,
                Var("n")
            ))

    def test_parser_bool(self):
        b1 = "x == 1"
        self.assertEqual(parse_expr(b1),
            BoolArithCmp(
                ArithCmp.Eq,
                Var("x"),
                ArithLit(1)))

        b2 = "x != 1"
        self.assertEqual(parse_expr(b2),
            BoolArithCmp(
                ArithCmp.Neq,
                Var("x"),
                ArithLit(1)))

        b3 = "x > 1"
        self.assertEqual(parse_expr(b3),
            BoolArithCmp(
                ArithCmp.Gt,
                Var("x"),
                ArithLit(1)))

    def test_parser_decl(self):
        decl = "long x;"
        self.assertEqual(parse_stm(decl),
            [StmDecl(tp_normal(AtomType.Long), 'x', None)]
        )

    def test_parser_decl_pointer(self):
        decl = "long* x;"
        self.assertEqual(parse_stm(decl),
            [StmDecl(
                tp_pointer(AtomType.Long),
                "x",
                None,
                VarKind.Local
            )]
        )

    def test_parser_decl_pointer_initialized(self):
        decl = "long* x = 0;"
        self.assertEqual(parse_stm(decl),
            [StmDecl(
                tp_pointer(AtomType.Long),
                "x",
                ArithLit(0),
                VarKind.Local
            )]
        )

    def test_parser_decl_pointer_initialized_address(self):
        decl = "long* x = &n;"
        self.assertEqual(parse_stm(decl),
            [
                StmDecl(
                    tp_pointer(AtomType.Long),
                    "x",
                    ArithUnaryop(
                        ArithUnaryOp.Addr,
                        Var("n")
                    ),
                    VarKind.Local
                )
            ]
        )

    def test_parser_decl_initialized(self):
        decl = "long x = 123;"
        self.assertEqual(parse_stm(decl),
            [StmDecl(tp_normal(AtomType.Long), 'x', ArithLit(num=123))]
        )

    def test_parser_fundef(self):
        input_str = "void foo(long a, int b) { }"
        output = FunDecl(tp_normal(AtomType.Void),
                    "foo",
                    [
                        FunArg(tp_normal(AtomType.Long), "a"),
                        FunArg(tp_normal(AtomType.Int), "b")
                    ],
                    [])

        self.assertEqual(parse_file(input_str), [output])

    def test_parser_fundef_return(self):
        input_str = "void foo(long a, int b) { return a; }"
        output = FunDecl(
            tp_normal(AtomType.Void),
                    "foo",
                    [
                        FunArg(tp_normal(AtomType.Long), "a"),
                        FunArg(tp_normal(AtomType.Int), "b")
                    ],
                    [StmReturn(Var("a"))])

        self.assertEqual(parse_file(input_str), [output])

    def test_parser_stm(self):
        s1 = "print(x);"
        self.assertEqual(parse_stm(s1),
            [StmPrint(Var("x"))])

        s1a = "print(x_);"
        self.assertEqual(parse_stm(s1a),
            [StmPrint(Var("x_"))])


        s2 = "print(15);"
        self.assertEqual(parse_stm(s2),
            [StmPrint(ArithLit(15))])

        s3 = "x = 1;"
        self.assertEqual(parse_stm(s3),
            [StmExpr(ArithAssign(lvalue_var("x"), ArithLit(1)))])

        s3a = "x += 1;"
        self.assertEqual(parse_stm(s3a),
            [StmExpr(ArithAssign(lvalue_var("x"),
                ArithBinop(
                    ArithOp.Add,
                    Var("x"),
                    ArithLit(1)
                )))])

        s3b = "x -= 1;"
        self.assertEqual(parse_stm(s3b),
            [StmExpr(ArithAssign(lvalue_var("x"),
                ArithBinop(
                    ArithOp.Sub,
                    Var("x"),
                    ArithLit(1)
                )))])

        s3c = "x *= 1;"
        self.assertEqual(parse_stm(s3c),
            [StmExpr(ArithAssign(lvalue_var("x"),
                ArithBinop(
                    ArithOp.Mul,
                    Var("x"),
                    ArithLit(1)
                )))])

        s3d = "x /= 1;"
        self.assertEqual(parse_stm(s3d),
            [StmExpr(ArithAssign(lvalue_var("x"),
                ArithBinop(
                    ArithOp.Div,
                    Var("x"),
                    ArithLit(1)
                )))])

        s3d = "x %= 1;"
        self.assertEqual(parse_stm(s3d),
            [StmExpr(ArithAssign(lvalue_var("x"),
                ArithBinop(
                    ArithOp.Mod,
                    Var("x"),
                    ArithLit(1)
                )))])

        s4 = "while (x == 1) {}"
        self.assertEqual(parse_stm(s4),
            [
                StmWhile(
                    BoolArithCmp(
                        ArithCmp.Eq,
                        Var("x"),
                        ArithLit(1)
                    ),
                    [])
            ])

        s5 = "while (x == 1) { x = x + 1; }"
        self.assertEqual(parse_stm(s5),
            [
                StmWhile(
                    BoolArithCmp(
                        ArithCmp.Eq,
                        Var("x"),
                        ArithLit(1)
                    ),
                    [
                        StmExpr(ArithAssign(lvalue_var("x"),
                            ArithBinop(
                                ArithOp.Add,
                                Var("x"),
                                ArithLit(1))
                            ))
                    ])
            ])

        s6 = "if (x == 1) {}"
        self.assertEqual(parse_stm(s6),
            [
                StmIf(
                    BoolArithCmp(
                        ArithCmp.Eq,
                        Var("x"),
                        ArithLit(1)
                    ),
                    [],
                    [])
            ])

        s7 = "if (x == 1) {} else {}"
        self.assertEqual(parse_stm(s7),
            [
                StmIf(
                    BoolArithCmp(
                        ArithCmp.Eq,
                        Var("x"),
                        ArithLit(1)
                    ),
                    [],
                    [])
            ])

        s8 = "{ }"
        self.assertEqual(parse_stm(s8),
            [
                StmBlock(
                    []
                )
            ])

        s9 = "break;"
        self.assertEqual(parse_stm(s9),
            [
                StmBreak()
            ])

        s10 = "continue;"
        self.assertEqual(parse_stm(s10),
            [
                StmContinue()
            ])

    def test_parse_stm_pointer_assign(self):
        s3e = "*n = 1;"
        self.assertEqual(parse_stm(s3e),
            [StmExpr(ArithAssign(
                lvalue_pointer("n"),
                ArithLit(1)
            ))])

        s3f = "*n += 1;"
        self.assertEqual(parse_stm(s3f),
            [StmExpr(ArithAssign(
                lvalue_pointer("n"),
                ArithBinop(
                    ArithOp.Add,
                    ArithUnaryop(
                        ArithUnaryOp.Deref,
                        Var("n")),
                    ArithLit(1)
                )
            ))])

    def test_parse_stm_deref(self):
        s3g = "n = &m;"
        self.assertEqual(parse_stm(s3g),
            [
                StmExpr(ArithAssign(
                    lvalue_var("n"),
                    ArithUnaryop(
                        ArithUnaryOp.Addr,
                        Var("m")
                    )
                ))
            ])

class ParserErrorTests(unittest.TestCase):
    def test_non_balanced_expr(self):
        inputs = [
            ")",
            "(1",
            "(1 + ()",
        ]
        for input in inputs:
            with self.subTest(i = input):
                with self.assertRaises(Exception):
                    parse_expr(input)

    def test_non_balanced_stm(self):
        inputs = [
            "while (1) {",
            "while (1) {} else",
            "while (1) {} else {",
            "if (1 {}",
            "if 1 {}",
            "x = 23",
            "x = ",
        ]
        for input in inputs:
            with self.subTest(i = input):
                with self.assertRaises(Exception):
                    parse_stm(input)

class RenameVarsTests(unittest.TestCase):
    def test_renamer(self):
        body1 = """
    long x;
    while (x == 0) {
        int x;
        if (x == 0) {
            long x;
        }
    }
    """

        body2 = """
    long x;
    while (x == 0) {
        int x2;
        if (x2 == 0) {
            long x3;
        }
    }
    """
        stms1 = parse_stm(body1)
        stms2 = parse_stm(body2)
        self.assertEqual(rename_vars(stms1), stms2)

class LocalVarsTests(unittest.TestCase):
    def test_function(self):
        body = """
    long x;
    long y = 1;
    int m = 0;
    if (x == 0) {
        long z;
    } else {
        long t;
    }
    while (x == x) {
        long a = 1;
    }
    """
        stms = parse_stm(body)
        local_vars = get_local_vars(stms)
        self.assertEqual(
            local_vars,
            ['x', 'y', 'm', 'z', 't', 'a'])

    def test_nested_block(self):
        body = """
    long x;
    if (0 == 0) {
        long x = 1;
    }
    """
        stms = parse_stm(body)
        local_vars = get_local_vars(stms)
        self.assertEqual(
            local_vars,
            ['x', 'x'])


if __name__ == "__main__":
    unittest.main()
