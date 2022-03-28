import pytest

import modules.txt2docx as t2d

from test.cases_cb import (testcode2, idealcode2,
                        testcode4, idealcode4,
                        testcode5, idealcode5,
                        testcode6, idealcode6)

def test_convert_basecode():

    return_code2 = t2d.convert_basecode(testcode2)
    assert "".join(return_code2) == "".join(idealcode2)

def test_convert_basecode2():

    return_code4 = t2d.convert_basecode(testcode4)
    assert "".join(return_code4) == "".join(idealcode4)


def test_convert_basecode5():

    return_code5 = t2d.convert_basecode(testcode5)
    assert "".join(return_code5) == "".join(idealcode5)


def test_convert_basecode6():

    return_code6 = t2d.convert_basecode(testcode6)
    assert "".join(return_code6) == "".join(idealcode6)

if __name__ == '__main__':
    pytest.main()
