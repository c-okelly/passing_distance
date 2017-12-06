import unittest

class BasicTest(unittest.TestCase):

    def test_upper(self):
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()