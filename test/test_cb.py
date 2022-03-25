import pytest

import modules.txt2docx as t2d

from test.cases_cb import (testcode2, idealcode2,
                        testcode4, idealcode4)

def test_convert_basecode():

    return_code2 = t2d.convert_basecode(testcode2)
    assert "".join(return_code2) == "".join(idealcode2)

def test_convert_basecode2():

    return_code4 = t2d.convert_basecode(testcode4)
    assert "".join(return_code4) == "".join(idealcode4)


if __name__ == '__main__':
    pytest.main()
