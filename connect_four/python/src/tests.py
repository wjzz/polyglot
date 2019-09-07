import unittest

from board import Board, Config

class BoardTest(unittest.TestCase):
    def test_eq(self):
        b = Board()
        self.assertTrue(b == b)
        b1 = b.apply_move(1)
        self.assertTrue(b1 == b1)
        self.assertTrue(b != b1)
        self.assertTrue(
            b.apply_move(5),
            b.apply_move(5)
        )

    def test_myhash(self):
        b1 = Board().apply_move(1).apply_move(2).apply_move(3)
        b2 = Board().apply_move(3).apply_move(2).apply_move(1)
        self.assertEqual(b1.myhash, b2.myhash)

        b3 = Board().apply_move(1)
        b4 = Board().apply_move(2)
        self.assertNotEqual(b3.myhash, b4.myhash)

        b5 = Board().apply_move(1).apply_move(4).apply_move(3).apply_move(2)
        b6 = Board().apply_move(3).apply_move(2).apply_move(1).apply_move(4)
        self.assertEqual(b5.myhash, b6.myhash)

    def test_pretty(self):
        b = Board()
        b.apply_move(5).apply_move(4).apply_move(3).apply_move(3)
        s = str(b)
        b1 = Board.from_str(s)
        self.assertTrue(b == b1)

    def test_legal_moves_start(self):
        b = Board()
        self.assertEqual(
            Config.COLS,
            len(b.legal_moves))

    def test_win(self):
        examples = [
            "6 .......\n"
            "5 .......\n"
            "4 .......\n"
            "3 .......\n"
            "2 .......\n"
            "1 .......\n"
            "last = None\n"
            ,
            # horizontal
            "6 .......\n"
            "5 .......\n"
            "4 .......\n"
            "3 .O.O.X.\n"
            "2 .O.OXO.\n"
            "1 .XOXXXX\n"
            "last = 6\n"
            ,
            # vertical
            "6 .......\n"
            "5 .......\n"
            "4 .O.....\n"
            "3 XO.....\n"
            "2 XO.....\n"
            "1 XOX....\n"
            "last = 1\n"
            ,
            "6 .....X.\n"
            "5 .....X.\n"
            "4 .....X.\n"
            "3 .O.O.X.\n"
            "2 .O.OXOO\n"
            "1 .XOXXXO\n"
            "last = 5\n"
            ,
            # diagonal
            "6 .......\n"
            "5 .......\n"
            "4 X......\n"
            "3 XX.....\n"
            "2 OXX....\n"
            "1 OOOXO..\n"
            "last = 0\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 X......\n"
            "3 XX.....\n"
            "2 OXX....\n"
            "1 OOOXO..\n"
            "last = 1\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 X......\n"
            "3 XX.....\n"
            "2 OXX....\n"
            "1 OOOXO..\n"
            "last = 2\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 X......\n"
            "3 XX.....\n"
            "2 OXX....\n"
            "1 OOOXO..\n"
            "last = 3\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 ....X..\n"
            "3 ...XX..\n"
            "2 .OXXO..\n"
            "1 .XOOO..\n"
            "last = 4\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 ....X..\n"
            "3 ...XX..\n"
            "2 .OXXO..\n"
            "1 .XOOO..\n"
            "last = 3\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 ....X..\n"
            "3 ...XX..\n"
            "2 .OXXO..\n"
            "1 .XOOO..\n"
            "last = 2\n"
            ,
            # non-wins
            "6 .......\n"
            "5 .......\n"
            "4 .....X.\n"
            "3 .O.O.X.\n"
            "2 .O.OXO.\n"
            "1 .XOXXXO\n"
            "last = 6\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 OX.....\n"
            "3 XO.....\n"
            "2 XO.....\n"
            "1 XO.....\n"
            "last = 1\n"
            ,
            "6 .....O.\n"
            "5 .....X.\n"
            "4 .....X.\n"
            "3 .O.O.X.\n"
            "2 .O.OXO.\n"
            "1 .XOXXXO\n"
            "last = 5\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 O......\n"
            "3 XX.....\n"
            "2 OXX....\n"
            "1 OOOX...\n"
            "last = 0\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 X......\n"
            "3 XO.....\n"
            "2 OXX....\n"
            "1 OOOX...\n"
            "last = 1\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 X......\n"
            "3 XX.....\n"
            "2 OXO....\n"
            "1 OOOX...\n"
            "last = 2\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 X......\n"
            "3 XX.....\n"
            "2 OXX....\n"
            "1 OOXOO..\n"
            "last = 3\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 ....O..\n"
            "3 ...XX..\n"
            "2 ..XXO..\n"
            "1 .XOOO..\n"
            "last = 4\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 ....X..\n"
            "3 ...OX..\n"
            "2 ..XXO..\n"
            "1 .XOOO..\n"
            "last = 3\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 ....X..\n"
            "3 ...XX..\n"
            "2 ..OXO..\n"
            "1 .XOOO..\n"
            "last = 2\n"
            ,
        ]
        results = [
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ]
        labels = [
            "empty",
            "horizontal",
            "vertical 1",
            "vertical 2",
            "diagonal 1",
            "diagonal 2",
            "diagonal 3",
            "diagonal 4",
            "diagonal 5",
            "diagonal 6",
            "diagonal 7",
            "non-win 1",
            "non-win 2",
            "non-win 3",
            "non-win 4",
            "non-win 5",
            "non-win 6",
            "non-win 7",
            "non-win 8",
            "non-win 9",
            "non-win 10",
        ]
        assert(len(examples) == len(results) == len(labels))
        
        for example, result, label in zip(examples, results, labels):
            with self.subTest(id=label):
                b = Board.from_str(example)
                self.assertEqual(
                    result,
                    b.is_win)

    def test_legal_moves_end(self):
        s = [ 
            "6 OOXOXOO\n"
            "5 OOOXXXX\n"
            "4 OXXOOXO\n"
            "3 XOXOOXX\n"
            "2 XOXOXXO\n"
            "1 XOXXOOX\n"
            "last = 5\n"
            ,
        ]
        b = Board.from_str(s[0])
        self.assertEqual(
            [],
            b.legal_moves)

    def test_str_hash(self):
        examples = [
            "6 .......\n"
            "5 .......\n"
            "4 .......\n"
            "3 .......\n"
            "2 .......\n"
            "1 .......\n"
            "last = None\n"
            ,
            # horizontal
            "6 .......\n"
            "5 .......\n"
            "4 .......\n"
            "3 .O.O.X.\n"
            "2 .O.OXO.\n"
            "1 .XOXXXX\n"
            "last = 6\n"
            ,
            # vertical
            "6 .......\n"
            "5 .......\n"
            "4 .O.....\n"
            "3 XO.....\n"
            "2 XO.....\n"
            "1 XOX....\n"
            "last = 1\n"
            ,
        ]

        results = [
            "......."
            "......."
            "......."
            "......."
            "......."
            "......."
            ,
            # horizontal
            "......."
            "......."
            "......."
            ".O.O.X."
            ".O.OXO."
            ".XOXXXX"
            ,
            # vertical
            "......."
            "......."
            ".O....."
            "XO....."
            "XO....."
            "XOX...."
            ,
        ]


        for i, (example, result) in enumerate(zip(examples, results)):
            with self.subTest(ex = i):
                self.assertEqual(result, 
                    Board.from_str(example).str_hash)


    def test_parsing(self):
        examples = [
            "6 .......\n"
            "5 .......\n"
            "4 .......\n"
            "3 .......\n"
            "2 .......\n"
            "1 .......\n"
            "last = None\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 .......\n"
            "3 .O.O.X.\n"
            "2 .O.OXOO\n"
            "1 .XOXXXX\n"
            "last = 3\n"
            ,
            "6 .....X.\n"
            "5 .....X.\n"
            "4 .....X.\n"
            "3 .O.O.X.\n"
            "2 .O.OXOO\n"
            "1 .XOXXXO\n"
            "last = 5\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 X......\n"
            "3 XX.....\n"
            "2 OXX....\n"
            "1 OOOXO..\n"
            "last = 0\n"
            ,
            "6 .......\n"
            "5 .......\n"
            "4 ....X..\n"
            "3 ...XX..\n"
            "2 .OXXO..\n"
            "1 .XOOO..\n"
            "last = 4\n"
            ,
        ]
        
        for example in examples:
            with self.subTest(ex = example):
                self.assertEqual(example, 
                    str(Board.from_str(example)))

if __name__ == "__main__":
    unittest.main()
