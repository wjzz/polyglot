import unittest

from board_full import Board, Config

class BoardFullTest(unittest.TestCase):
    def test_empty_board(self):
        Board()

    def test_succesors(self):
        """
        Checks that the number of generated boards is correct.
        """
        b = Board()

        self.assertEqual(1, 
            len(list(b.succesors(0))))

        self.assertEqual(b,
            next(b.succesors(0)))
  
        self.assertEqual(1 + Config.COLS, 
            len(list(b.succesors(1))))

        self.assertEqual(1 + Config.COLS + Config.COLS ** 2,
            len(list(b.succesors(2))))
 
    def test_succesors_mut_and_immut_equivalent(self):
        """
        Checks that the two version of the succesors return the same nodes.
        """
        depth = 4
        immut_gen = Board().succesors(depth)
        mut_gen = Board().succesors_mut(depth)

        for b, str_hash in zip(immut_gen, mut_gen):
            self.assertEqual(b.str_hash, str_hash)

    def test_visit_all_mut(self):
        total = 0
        def visitor(board):
            nonlocal total
            total += 1
        
        total = 0
        Board().visit_all_mut(0, visitor)
        self.assertEqual(total, 1)

        total = 0
        Board().visit_all_mut(1, visitor)
        self.assertEqual(total, 1 + Config.COLS)

        TOTAL_76_DEPTH_5 = 19608
        total = 0
        Board().visit_all_mut(5, visitor)
        self.assertEqual(total, TOTAL_76_DEPTH_5)

        # NOTE: this is a bit too slow for a unit test
        # TOTAL_76_DEPTH_7 = 960793
        # total = 0
        # Board().visit_all_mut(7, visitor)
        # self.assertEqual(total, TOTAL_76_DEPTH_7)

    def test_make_unmake(self):
        """
        Checks that make and unmake are inverses of each other.
        """
        # bigger than 4 can be a little bit to slow for a unit test
        MAX_DEPTH = 4

        for board in Board().succesors(MAX_DEPTH):
            str1 = board.str_hash
            for move in board.legal_moves:
                board.make_move(move)
                str3 = board.myhash
                self.assertNotEqual(str1, str3)

                board.unmake_move(move)
                str2 = board.str_hash
                self.assertEqual(str1, str2)

    #@unittest.skip    
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

    @unittest.skip
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

    #@unittest.skip
    def test_pretty(self):
        b = Board()
        b.apply_move(5).apply_move(4).apply_move(3).apply_move(3)
        s = str(b)
        b1 = Board.from_str(s)
        self.assertTrue(b == b1)
    
    #@unittest.skip
    def test_legal_moves_start(self):
        b = Board()
        self.assertEqual(
            Config.COLS,
            len(b.legal_moves))

    #@unittest.skip
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
            "last = 0\n"
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
            "2 OXO....\n"
            "1 OOXXO..\n"
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

    #@unittest.skip
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
    
    #@unittest.skip
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

    #@unittest.skip
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
