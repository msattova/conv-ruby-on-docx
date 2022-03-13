import unittest

import modules.txt2docx as t2d

from test.cases import testcode, idealcode, testcode2, idealcode2, testcode3, idealcode3

class UnitTest(unittest.TestCase):

    def test_convert_basecode(self):
        return_code = t2d.convert_basecode(testcode)
        self.assertEqual("".join(return_code), "".join(idealcode))
        return_code2 = t2d.convert_basecode(testcode2)
        self.assertEqual("".join(return_code2), "".join(idealcode2))

        return_code3 = t2d.convert_basecode(testcode3)
        print("\t ret: ", "".join(return_code3))
        print("\t ideal: ", "".join(idealcode3))
        self.assertEqual("".join(return_code3), "".join(idealcode3))


if __name__ == '__main__':
    unittest.main()
