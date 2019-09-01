import unittest

class Tests(unittest.TestCase):
    # this is called before every test
    def setUp(self):
        self.ex = 123

    @unittest.SkipTest
    def test_many(self):
        for i in range(10):
            # this gives us a special msg
            # so that we know which case failed
            with self.subTest(i = i):
                self.assertTrue(i % 2 == 0)
    
    def test_raising(self):
        with self.assertRaises(TypeError):
            "123" - 12

    def test_example(self):
        self.assertEqual(123, self.ex)

    def test_init(self):
        self.assertTrue(True)

    @unittest.SkipTest
    def test_not_working(self):
        self.assertTrue(False)

    
if __name__ == "__main__":
    unittest.main(verbosity=2)
